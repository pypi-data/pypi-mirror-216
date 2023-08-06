"""Manage media in the understory."""

import pathlib
import subprocess

import web
import yt_dlp

app = web.application(
    __name__,
    prefix="media",
    args={"filename": rf"{web.nb60_re}{{4}}.\w{{1,10}}"},
    model={"media": {"mid": "TEXT", "sha256": "TEXT UNIQUE", "size": "INTEGER"}},
)

media_dir = pathlib.Path("media")
media_dir.mkdir(exist_ok=True)


@app.wrap
def linkify_head(handler, main_app):
    yield
    if web.tx.request.uri.path == "":
        web.add_rel_links(**{"media-endpoint": "/media"})


@app.query
def get_media(db):
    """Return a list of media filepaths."""
    try:
        filepaths = list(media_dir.iterdir())
    except FileNotFoundError:
        filepaths = []
    return filepaths


@app.query
def create_file(db):
    """Create a media file."""
    media_id = get_media_id()
    try:
        filepath = web.form("file").file.save(media_dir / media_id)
    except web.BadRequest:
        file_details = web.tx.request.body._data
        filepath = pathlib.Path(file_details["name"]).with_stem(media_id)
        # XXX with (media_dir / filepath).open("wb") as fp:
        # XXX     fp.write(b"-" * file_details["size"])
    else:
        index(filepath)
    return filepath.name


def get_media_id():
    db = app.model.db
    while True:
        media_id = web.nbrandom(4)
        try:
            db.insert(
                "media",
                mid=media_id,
            )
        except db.IntegrityError:
            pass
        else:
            break
    return media_id


def download(url):
    media_id = get_media_id()
    options = {"outtmpl": str(media_dir / f"{media_id}.%(ext)s")}
    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info_dict)
    index(filepath)


def index(filepath):
    filepath = pathlib.Path(filepath)
    if str(filepath).endswith(".heic"):
        subprocess.Popen(
            [
                "convert",
                filepath,
                "-set",
                "filename:base",
                "%[basename]",
                f"{media_dir}/%[filename:base].jpg",
            ]
        )
    sha256 = subprocess.getoutput(f"sha256sum {filepath}").split()[0]
    media_id = filepath.stem
    try:
        web.tx.db.update(
            "media",
            sha256=sha256,
            size=filepath.stat().st_size,
            where="mid = ?",
            vals=[media_id],
        )
    except web.tx.db.IntegrityError:
        web.tx.db.delete("media", where="mid = ?", vals=[media_id])
        filepath.unlink()


@app.query
def get_filepath(db, filename):
    """Return a media file's path."""
    return media_dir / filename


@app.query
def delete_file(db, filename):
    """Delete given file."""
    filepath = app.model.get_filepath(filename)
    db.delete("media", where="mid = ?", vals=[filepath.stem])
    filepath.unlink()


@app.control("")
class MediaEndpoint:
    """Your media files."""

    # owner_only = ["post"]

    def get(self):
        """Render a list of your media files."""
        media = app.model.get_media()
        try:
            query = web.form("q").q
        except web.BadRequest:
            pass
        else:
            if query == "source":
                # {
                #   "url": "https://media.aaronpk.com/2020/07/file-20200726XXX.jpg",
                #   "published": "2020-07-26T09:51:11-07:00",
                #   "mime_type": "image/jpeg"
                # }
                return {
                    "items": [
                        {
                            "url": f"{web.tx.origin}/media/{filepath.name}",
                            "published": "TODO",
                            "mime_type": "TODO",
                        }
                        for filepath in media
                    ]
                }
        return app.view.index(media)

    def post(self):
        """Create a media file."""
        try:
            form = web.form("url")
            web.enqueue(download, form.url)
            raise web.Accepted("download enqueued")
        except web.BadRequest:
            filename = app.model.create_file()
            raise web.Created(
                app.view.media_added(filename), f"{web.tx.origin}/media/{filename}"
            )


@app.control("{filename}")
class MediaFile:
    """A media file."""

    owner_only = ["delete"]

    def get(self, filename):
        """Return media with given filename."""
        return media_dir / filename

    def put(self, filename):
        """Upload a chunk of a media file."""
        content_range, _, total_filesize = (
            str(web.tx.request.headers["Content-Range"])
            .partition(" ")[2]
            .partition("/")
        )
        content_start, _, content_end = content_range.partition("-")
        content_start = int(content_start)
        content_end = int(content_end)
        total_filesize = int(total_filesize)
        filepath = media_dir / filename
        # XXX with filepath.open("rb+") as fp:
        with filepath.open("ab") as fp:
            # XXX fp.seek(content_start)
            fp.write(web.tx.request.body)
        if content_end == total_filesize:
            index(filepath)
        raise web.OK("")
        # raise web.Created(
        #     app.view.media_added(filename), f"{web.tx.origin}/media/{filename}"
        # )

    def delete(self, filename):
        """Delete media with given filename."""
        app.model.delete_file(filename)
        return app.view.media_deleted()

from __future__ import annotations

from typing import Any

from actions.task_runner import (
    delete_temp_files,
    download_images,
    download_pdfs,
    open_google,
    open_youtube,
    rename_files,
    search_google,
    search_youtube,
    send_email,
    start_scheduler,
    take_screenshot,
    voice_command,
    web_scrape,
    write_to_file,
)
from plugins.base import Plugin


class OpenYouTubePlugin(Plugin):
    name = "open_youtube"
    description = "Open YouTube"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return open_youtube(*args, **kwargs)


class RenameFilesPlugin(Plugin):
    name = "rename_files"
    description = "Rename files in a folder"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return rename_files(*args, **kwargs)


class DeleteTempFilesPlugin(Plugin):
    name = "delete_temp_files"
    description = "Delete temp files in a folder"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return delete_temp_files(*args, **kwargs)


class SearchYouTubePlugin(Plugin):
    name = "search_youtube"
    description = "Search YouTube"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return search_youtube(*args, **kwargs)


class DownloadPdfsPlugin(Plugin):
    name = "download_pdfs"
    description = "Download PDFs from a URL"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return download_pdfs(*args, **kwargs)


class SendEmailPlugin(Plugin):
    name = "send_email"
    description = "Send an email"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return send_email(*args, **kwargs)


class StartSchedulerPlugin(Plugin):
    name = "start_scheduler"
    description = "Start the scheduler"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return start_scheduler(*args, **kwargs)


class OpenGooglePlugin(Plugin):
    name = "open_google"
    description = "Open Google"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return open_google(*args, **kwargs)


class SearchGooglePlugin(Plugin):
    name = "search_google"
    description = "Search Google"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return search_google(*args, **kwargs)


class DownloadImagesPlugin(Plugin):
    name = "download_images"
    description = "Download images"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return download_images(*args, **kwargs)


class TakeScreenshotPlugin(Plugin):
    name = "take_screenshot"
    description = "Capture a screenshot"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return take_screenshot(*args, **kwargs)


class WriteToFilePlugin(Plugin):
    name = "write_to_file"
    description = "Write content to a file"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return write_to_file(*args, **kwargs)


class VoiceCommandPlugin(Plugin):
    name = "voice_command"
    description = "Run a voice command"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return voice_command(*args, **kwargs)


class WebScrapePlugin(Plugin):
    name = "web_scrape"
    description = "Scrape a webpage"

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return web_scrape(*args, **kwargs)

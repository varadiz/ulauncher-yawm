from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
import subprocess


class WindowManagerExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        subprocess.run(["wmctrl", "-a", data["win_id"], "-i"])


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        result = subprocess.run(
            ["wmctrl", "-l"], capture_output=True, text=True).stdout
        windows = result.split("\n")
        items = []

        # TODO should filter results based on query: event.get_query()
        for win in windows:
            win_id = win.split(" ")[0]
            win_name = " ".join(win.split(" ")[3:])

            data = {"win_id": win_id}
            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name=win_name,
                description=win_name,
                on_enter=ExtensionCustomAction(data, keep_app_open=True)
            ))

        return RenderResultListAction(items)


if __name__ == '__main__':
    WindowManagerExtension().run()

import os

from gi.repository import Adw, Gio, GLib, Gtk

from core.config import load_yaml, write_yaml
from core.mod_manager import load_metadata, refresh_mod_links

class GameSettingsWindow(Adw.Window):
    def __init__(self, parent_window, staging_path, **kwargs):
        super().__init__(title=_("Settings"), transient_for=parent_window, modal=True, **kwargs)
        self.set_default_size(500, -1)
        staging_meta_path = os.path.join(staging_path, ".staging.nomm.yaml")
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20, margin_top=24, margin_bottom=24, margin_start=24, margin_end=24)
        self.set_content(content)
        
        general_group = Adw.PreferencesGroup(title=_(f"{self.dashboard.game} Settings"))
        content.append(general_group)
        
        # Hardlink
        use_hardlink = Adw.SwitchRow(title=_("Use Hardlinks"))
        use_hardlink.set_subtitle(_("Improves compatibility for some games"))
        use_hardlink.set_active(load_yaml(staging_meta_path)["settings"].get('enable_hardlinks', False))
        use_hardlink.connect("notify::active", lambda row, pspec: toggle_setting(self, staging_meta_path, 'enable_hardlinks', row.get_active()))
        general_group.add(use_hardlink)
        
        content.append(Gtk.Separator(margin_top=10))
        
        save_btn = Gtk.Button(label=_("Close"), css_classes=["suggested-action"], margin_top=12)
        save_btn.connect("clicked", lambda b: self.close_settings())
        content.append(save_btn)
        
        def toggle_setting(self, staging_meta_path, key, state):
            # Get the staging metadata config then change the enable_hardlinks settings
            staging_metadata = load_metadata(staging_meta_path)
            staging_metadata["settings"][key] = state
            write_yaml(staging_metadata, staging_meta_path)
            
            #if key == "enable_hardlinks":
            #    mod_list = staging_metadata.get("mods")
            #    # if "deployment_target" in mod_meta:
            #    #     for target in deployment_targets:
            #    #         if target["name"] == mod_meta["deployment_target"]:
            #    #             dest_dir = target["path"]
            #    #             break
            #    
            #    refresh_mod_links(staging_path, dest_dir, mod_list)
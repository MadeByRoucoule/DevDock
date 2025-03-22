import json

class SettingsScript:
    def __init__(self):
        self.settings = self.get_settings()

    def get_settings(self):
        with open("src/json/settings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    
    def get_setting_value(self, key):
        keys = key.split(".")
        ref = self.settings
        for k in keys:
            ref = ref.get(k)
            if ref is None:
                return None
        
        if isinstance(ref, dict):
            if set(ref.keys()) == {"state", "from", "to"}:
                return ref["state"]
            else:
                for option, value in ref.items():
                    if value == 1:
                        return option
                return list(ref.keys())[0] if ref else None
        else:
            return ref

    def change_setting(self, key, new_value):
        keys = key.split(".")
        ref = self.settings
        for k in keys[:-1]:
            ref = ref.get(k, {})
        final_key = keys[-1]
        
        if final_key not in ref:
            print(f"Clé '{final_key}' introuvable dans la catégorie.")
            return

        current_value = ref[final_key]
        if isinstance(current_value, dict):
            if set(current_value.keys()) == {"state", "from", "to"}:
                ref[final_key]["state"] = new_value
            elif new_value in current_value:
                for opt in current_value:
                    ref[final_key][opt] = 1 if opt == new_value else 0
            else:
                ref[final_key] = new_value
        else:
            ref[final_key] = new_value
        
        self.save_settings()

    def save_settings(self):
        with open("src/json/settings.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

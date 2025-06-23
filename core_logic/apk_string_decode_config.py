from pathlib import Path


class Config:
    _base_download_path = Path.home() / "Downloads" # Set default to Downloads folder

    @classmethod
    def set_download_path(cls, new_path):
        cls._base_download_path = Path(new_path)

    @classmethod
    def get_download_path(cls):
        return cls._base_download_path

    @classmethod
    def get_str_download_path(cls):
        return str(cls._base_download_path) + "/"

    @classmethod
    def get_extracted_folder(cls):
        return cls.get_str_download_path() + "apk_extracted/"

    @classmethod
    def get_manifest_path(cls):
        return cls.get_extracted_folder() + "AndroidManifest.xml"

    @classmethod
    def get_smali_folder(cls):
        return cls.get_extracted_folder() + "smali/"

    @classmethod
    def get_modified_apk(cls):
        return cls.get_str_download_path() + "modified_extract_app.apk"

    @classmethod
    def get_decoded_apk(cls):
        return cls.get_str_download_path() + "decoded_app.apk"

    @classmethod
    def get_missing_strings_path(cls):
        return cls.get_str_download_path() + "missing_strings.json"

    @classmethod
    def get_backup_path(cls):
        return cls.get_str_download_path() + "apk_extracted_backup/"

    @classmethod
    def get_manifest_backup(cls):
        return cls.get_backup_path() + "AndroidManifest.xml"

    @classmethod
    def get_res_folder(cls):
        return cls.get_extracted_folder() + "res/"

    @classmethod
    def get_public_xml_path(cls):
        return cls.get_res_folder() + "values/public.xml"
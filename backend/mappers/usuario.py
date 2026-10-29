class UsuarioMapper:
    @staticmethod
    def map_foto_perfil(foto_perfil_path: str | None) -> str | None:
        if foto_perfil_path:
            return "/" + foto_perfil_path.replace("\\", "/").lstrip("/")

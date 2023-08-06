class FileFinderError(Exception):
    """Classe mãe paa tratar todas as exceções do programa"""
    pass

class InvalidInputError(FileFinderError):
    """Classe específica para erros que aconteçam devido a inputs do usuario"""
    pass

class ZeroFilesFoundError(FileFinderError):
    """Classe especifica para erros ocorridos ao não encontrar nenhum arquivo"""
    pass
from django.apps import AppConfig


class PricesAnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prices_analyzer'
    
    def ready(self) -> None:
        import prices_analyzer.signals # noqa: F401

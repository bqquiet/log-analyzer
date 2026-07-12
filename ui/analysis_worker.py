from PyQt5.QtCore import QThread, pyqtSignal

from models.log_analyzer import LogAnalyzer


class AnalysisWorker(QThread):
    progress_changed = pyqtSignal(int, str)
    finished_successfully = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, file_path, patterns):
        super().__init__()
        self.file_path = file_path
        self.patterns = patterns

    def run(self):
        try:
            analyzer = LogAnalyzer()
            analyzer.load_file(self.file_path, progress_callback=self.report_load_progress)
            analyzer.analyze(self.patterns, progress_callback=self.report_analyze_progress)
            self.finished_successfully.emit(analyzer)
        except Exception as error:
            self.failed.emit(str(error))

    def report_load_progress(self, percent):
        overall = int(percent * 0.4)
        self.progress_changed.emit(overall, "Читання файлу...")

    def report_analyze_progress(self, percent):
        overall = 40 + int(percent * 0.6)
        self.progress_changed.emit(overall, "Пошук підозрілих записів...")
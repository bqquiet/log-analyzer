import json
from datetime import datetime


class FileStorage:
    @staticmethod
    def write_json_report(path, report_data):
        report_data = dict(report_data)
        report_data["analyzed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def write_txt_report(path, report_data):
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Джерело: {report_data.get('source_file')}\n")
            f.write(f"Час аналізу: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("Статистика:\n")
            for level, count in report_data.get("statistics", {}).items():
                f.write(f"  {level}: {count}\n")
            f.write("\nЗнайдені записи:\n")
            for entry in report_data.get("entries", []):
                f.write(f"  [{entry['line']}] {entry['level']}: {entry['text']}\n")

    @staticmethod
    def read_json(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
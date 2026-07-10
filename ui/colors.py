CATEGORY_COLORS = {
    "Error": {"bg": "#fdecea", "border": "#ef5350", "text": "#c62828"},
    "Denied": {"bg": "#fff8e1", "border": "#ffca28", "text": "#f57f17"},
    "Failed": {"bg": "#e3f2fd", "border": "#42a5f5", "text": "#1565c0"},
    "Warning": {"bg": "#e8f5e9", "border": "#66bb6a", "text": "#2e7d32"},
}

DEFAULT_CATEGORY_COLOR = {"bg": "#f5f5f5", "border": "#bdbdbd", "text": "#616161"}


def get_category_color(category):
    return CATEGORY_COLORS.get(category, DEFAULT_CATEGORY_COLOR)
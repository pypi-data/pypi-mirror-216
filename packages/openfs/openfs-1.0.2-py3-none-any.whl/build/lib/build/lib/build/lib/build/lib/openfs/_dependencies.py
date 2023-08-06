
def _try_optional_dependencies():
    try:
        import ipywidgets
        from IPython.display import display, Code
        
        return True
    except ImportError:
        return False
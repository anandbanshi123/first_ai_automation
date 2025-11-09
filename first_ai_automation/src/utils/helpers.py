def take_screenshot(page, file_name):
    page.screenshot(path=file_name)

def log_message(message):
    print(message)

def wait_for_element(page, selector, timeout=30000):
    page.wait_for_selector(selector, timeout=timeout)
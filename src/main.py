from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from output_tabs import OutputTabs
from input_tabs import InputTabs
from request_bar import RequestBar
from utils import parse_json_body
import sys, requests, json
from bs4 import BeautifulSoup as bs

class SimplePythonRequests(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Python Requests")
        self.setGeometry(100, 100, 1200, 800)
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.request_bar = RequestBar()
        main_layout.addLayout(self.request_bar)
        self.input_tab_widget = InputTabs()
        main_layout.addWidget(self.input_tab_widget)
        self.output_tab_widget = OutputTabs()

        main_layout.addWidget(self.output_tab_widget)
        self.setCentralWidget(main_widget)
        # Connect signals
        self.request_bar.send_button.clicked.connect(self.send_request)
        self.request_bar.url_input.returnPressed.connect(self.send_request)
    
    def send_request(self):
        current_url = self.request_bar.url_input.text()
        if current_url.replace("http://", "").replace("https://", "") != "":
            try:
                method = self.request_bar.http_verb.currentText()
                url = self.request_bar.url_input.text()
                headers = self.input_tab_widget.get_headers()
                params = self.input_tab_widget.get_params()
                content_type = self.input_tab_widget.get_content_type()
                body = self.input_tab_widget.get_body()
                
                request_kwargs = {
                    "method": method,
                    "url": url,
                    "headers": headers,
                    "params": params,
                }
                
                if content_type:
                    headers["Content-Type"] = content_type
                    if content_type == "application/json":
                        try:
                            json_data = parse_json_body(body)
                            if isinstance(json_data, str):
                                self.output_tab_widget.response_text.setText(json_data)
                                return
                            request_kwargs['json'] = json_data
                        except Exception as e:
                            self.output_tab_widget.response_text.setText(f"Error parsing JSON: {str(e)}")
                            return
                    elif content_type == "application/x-www-form-urlencoded":
                        request_kwargs['data'] = body
                        
                r = requests.request(**request_kwargs)
                formatted_headers = self.format_headers(r.headers)
                self.output_tab_widget.headers_text.setPlainText(formatted_headers)
                
                formatted_response = self.format_response(r)
                self.output_tab_widget.response_text.setPlainText(formatted_response)
            except requests.RequestException as e:
                self.output_tab_widget.response_text.setText(f"Error sending request: {str(e)}")
        else:
            return self.output_tab_widget.response_text.setText("Could not send request")
            # dummyjson.com/test
            
    def format_headers(self, headers):
        return "\n".join([f"{k}: {v}" for k, v in headers.items()])
    
    def format_response(self, response):
        content_type = response.headers.get("Content-Type", "").lower()
        
        if "text/html" in content_type:
            soup = bs(response.text, 'html.parser')
            return soup.prettify()
        else:
            if "application/json" in content_type:
                try:
                    return json.dumps(response.json(), indent=2)
                except json.JSONDecodeError:
                    return response.text

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimplePythonRequests()
    window.show()
    sys.exit(app.exec())
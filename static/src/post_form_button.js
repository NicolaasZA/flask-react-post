'use strict';

const b = React.createElement;

class PostFormButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return b(
      'button',
      { onClick: () => this.sendRequest() },
      'Send Form'
    );
  }

  sendRequest() {
    // Hierdie is het jy form data na die backend stuur. Check serve.py om te sien hoe die form data gelees word.
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/", true);

    var formData = new FormData();
    formData.append("fieldA", "valueA");
    formData.append("fieldB", 300);

    // Hierdie is net om die response te wys in die preview iframe
    xhr.onreadystatechange = (ev) => { 
      var resultHTML = xhr.responseText;
      this.updatePreview(resultHTML);
    };

    xhr.send(formData);
  }

  updatePreview(html) {
    document.getElementById("previewFrame").remove();

    var iframe = document.createElement('iframe');
    iframe.id = 'previewFrame';
    iframe.srcdoc = html;
    iframe.src = "data:text/html;charset=utf-8," + escape(html);
    document.getElementById('previewContainer').appendChild(iframe);
  }
}

const formButtonContainer = document.querySelector('#post_form_button_container');
ReactDOM.render(b(PostFormButton), formButtonContainer);
'use strict';

const c = React.createElement;

class PostJSONButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return c(
      'button',
      { onClick: () => this.sendRequest() },
      'Send JSON'
    );
  }

  sendRequest() {
    var url = "http://127.0.0.1:5000/";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    const bodyObject = {
      // Sit data hier binne
      fieldA: "valueA",
      fieldB: 300.25
    };

    // Hierdie is net om die response te wys in die preview iframe
    xhr.onreadystatechange = (ev) => { 
      var resultHTML = xhr.responseText;
      this.updatePreview(resultHTML);
    };

    xhr.send(JSON.stringify(bodyObject));
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

const jsonButtonContainer = document.querySelector('#post_json_button_container');
ReactDOM.render(c(PostJSONButton), jsonButtonContainer);
'use strict';

const a = React.createElement;

class PostQueryButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return a(
      'button',
      { onClick: () => this.sendRequest() },
      'Send Query'
    );
  }

  sendRequest() {
    // Hierdie is hoe jy met query parameters werk. 
    // Hierdie parameters is visible en kan deur network sniffers gelees word, so MOENIE vir sensitiewe of personal data gebruik nie
    const params = "?fieldA=valueA&fieldB=300";

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/" + params, true);

    // Hierdie is net om die response te wys in die preview iframe
    xhr.onreadystatechange = (ev) => { 
      var resultHTML = xhr.responseText;
      this.updatePreview(resultHTML);
    };


    xhr.send();
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

const queryButtonContainer = document.querySelector('#post_query_button_container');
ReactDOM.render(a(PostQueryButton), queryButtonContainer);
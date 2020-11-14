var cors_api_url = 'https://cors-anywhere.herokuapp.com/';
  function doCORSRequest(options, printResult) {
    var x = new XMLHttpRequest();
    x.open(options.method, cors_api_url + options.url);
    x.onload = x.onerror = function() {
      printResult(
        (x.responseText||'')
      );
    };
    if (/^POST/i.test(options.method)) {
      x.setRequestHeader('Content-Type', 'application/json');
    }
    x.send(options.data);
  }

/**
 * Helper function for POSTing data as JSON with fetch.
 *
 * @param {Object} options
 * @param {string} options.url - URL to POST data to
 * @param {FormData} options.formData - `FormData` instance
 * @return {Object} - Response body from URL that was POSTed to
 */
async function postFormDataAsJson({ url, formData }) {
	const plainFormData = Object.fromEntries(formData.entries());
	const formDataJsonString = JSON.stringify(plainFormData);
  var output ='';
  doCORSRequest({
        method: 'POST',
        url: url,
        data: formDataJsonString
      }, function printResult(result) {
    		output = result.replace("{\"resultado\":\"", "");
    		output = output.replace("\"}", "");
    		var newline = String.fromCharCode(13, 10);
    		output = output.replaceAll('\\n', newline);
    		output = output.replaceAll('\\u00f3', 'ó');
    		output = output.replaceAll('\\u00e9', 'é');
    		output = output.replaceAll('\\u00ed', 'í');
    		output = output.replaceAll('\\u00e1', 'á');
    		output = output.replaceAll('\\u00fa', 'ú');
    		output = output.replaceAll('\\u00d3', 'Ó');
    		output = output.replaceAll('\\u00c9', 'É');
    		output = output.replaceAll('\\u00ed', 'í');
    		output = output.replaceAll('\\u00c1', 'Á');
    		output = output.replaceAll('\\u00da', 'Ú');
        output = output.replaceAll('\\u00f1', 'ñ');
    		output = output.replaceAll('\\u00d1', 'Ñ');
    		document.getElementById("id01").value = output;
      });
  return output;
}

/**
 * Event handler for a form submit event.
 *
 * @see https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/submit_event
 *
 * @param {SubmitEvent} event
 */
async function handleFormSubmit(event) {
	event.preventDefault();

	const form = event.currentTarget;
	const url = form.action;

	try {
		const formData = new FormData(form);
		const responseData = await postFormDataAsJson({ url, formData });

		console.log({ responseData });
	} catch (error) {
		console.error(error);
	}
}

const getForm = document.getElementById("form-predict");
getForm.addEventListener("submit", handleFormSubmit);
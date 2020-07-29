// Populate the groups on the main page
export function getGroups() {
  var groupList = document.querySelector('#route-collection');

  var request = new XMLHttpRequest();
  request.open('POST', '/viewAvailableRouteGroups', true);
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      // Success!
      var data = JSON.parse(request.responseText);
      const groups = data['groups'];
      var outputHtml = '';
      for (var group in groups) {
        outputHtml += '<div class="expand-route-link">';
        outputHtml +=
          '<p>' +
          Object.values(groups[group]) +
          ' ' +
          Object.keys(groups[group]);
        outputHtml += `<button id=${Object.keys(
          groups[group]
        )} onclick='deleteRouteGroup(this.id)'>Delete </button>`;
        outputHtml += '</p>';
        outputHtml += '</div>\n';
      }

      outputHtml +=
        '<button class="pure-button pure-button-primary">+ Add More</button>';

      groupList.innerHTML = outputHtml;

      // TODO: This needs to be an awaitable in the future
      document
        .querySelector('#route-collection > .pure-button')
        .addEventListener('click', moveToObjectCreation, false);
    } else {
      // We reached our target server, but it returned an error
    }
  };

  request.onerror = function() {
    // There was a connection error of some sort
  };

  var jsonData = { userId: localStorage['userId'] };

  request.send(JSON.stringify(jsonData));
}

export async function deleteRouteGroup(objectId) {
  await fetch(`/deleteRouteGroup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      userId: localStorage['userId'],
      objectId: objectId,
    }),
  }).catch((err) => {
    console.log('Error:', err);
    return false;
  });
}

export async function getRouteGroup(objectId) {
  let response = await fetch(`/getRouteGroup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      userId: localStorage['userId'],
      objectId: objectId,
    }),
  }).catch((err) => {
    console.log('Error:', err);
    return false;
  });

  let resStream = response.json();
  return resStream;
}

/*
EXAMPLE of updatedRouteGroup: {"userId":"7019", "objectName": "randomName", "apiId": "0", "isCRUD":true, "isReadMultiple":false, "isSingleRoute":true}
*/
export async function updateRouteGroup(objectId, updatedRouteGroup) {
  let resStream = await fetch(`/updateRouteGroup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ updatedRouteGroup, objectId }),
  }).catch((err) => {
    console.log('Error:', err);
    return false;
  });
  if (resStream.status === 200) {
    return true;
  }
  return false;
}

export function addGroupRoute() {
  // initialize request
  var request = new XMLHttpRequest();
  request.open('POST', '/addNewRouteGroup');
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

  // form the request json
  var data = {
    userId: localStorage['userId'],
    objectName: variableHandling(
      document.querySelector('#object-name').value,
      'class'
    ),
    apiId: 0, //TO DO: Match routegroup apiId with proper apiId when multiple APIs exist
    isCRUD: document.querySelector('#crud-bool').innerText == 'Yes',
    isReadMultiple:
      document.querySelector('#read-multiple-bool').innerText == 'Yes',
    isReadAllObjects:
      document.querySelector('#read-objects-bool').innerText == 'Yes',
    isSingleRoute:
      document.querySelector('#single-route-bool').innerText == 'Yes',
  };

  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      // Success!
      var data = JSON.parse(request.responseText);
      const objectId = data['objectId'];
      console.log(objectId);

      // Store the new objectId in cache
      localStorage['currentObjectId'] = objectId;

      // Move the page to defining the attributes
      moveToObjectAttributeCreation();
    } else {
      // We reached our target server, but it returned an error
      alert('Enter an Object Name!');
    }
  };

  request.onerror = function() {
    // There was a connection error of some sort
  };

  request.send(JSON.stringify(data));
}

export async function getObjectAttributes(objectId) {
  let response = await fetch(`/getObjectAttributes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      userId: localStorage['userId'],
      objectId: objectId,
    }),
  }).catch((err) => {
    console.log('Error:', err);
    return false;
  });

  let resStream = response.json();
  return resStream;
}

export async function deleteObjectAttribute(attributeId) {
  await fetch(`/deleteObjectAttribute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userId: localStorage['userId'], attributeId }),
  }).catch((err) => {
    console.log('Error:', err);
    return false;
  });
}

/*
EXAMPLE of updatedObjectAttribute: {"name": "randomName", "type": "number", "description":"a new one", "isUnique":true, "isEncrypted":true, "generationMethod": "", "isNullable": false}
*/
export async function updateObjectAttribute(
  attributeId,
  updatedObjectAttribute
) {
  let resStream = await fetch(`/updateObjectAttribute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      updatedObjectAttribute,
      attributeId,
      userId: localStorage['userId'],
    }),
  }).catch((err) => {
    console.log('Error:', err);
    return false;
  });
  if (resStream.status === 200) {
    return true;
  }
  return false;
}

export function flipBoolButton(event) {
  console.log(event);
  if (event.srcElement.innerText == 'Yes') {
    event.srcElement.className = 'bool-button pure-u-1-3 pure-button';
    event.srcElement.innerHTML = 'No';
  } else {
    event.srcElement.className =
      'bool-button pure-u-1-3 pure-button pure-button-active';
    event.srcElement.innerHTML = 'Yes';
  }
}

let isDropdownFocused = false;
let attrNumber = 0;
export function addAdditionalAttributeSpace() {
  attrNumber++;
  const additionalAttrSection = `
<tr>
    <td>
        <input id="attr-text-field${attrNumber}" class="attribute-name" type="text" value="" />
    </td>
    <td>
        <form class="pure-form pure-form-stacked">
            <select class="type" id="dropdown${attrNumber}" >
                <option>number</option>
                <option>decimal</option>
                <option>word(s)</option>
                <option>true / false</option>
                <option>date and time</option>
            </select>
        </form>
    </td>
</tr>
`;

  var tableToAppend = document.querySelector('.object-attribute-table');
  var newRow = tableToAppend.insertRow(-1);
  newRow.innerHTML += '\n' + additionalAttrSection;
  document.querySelector(`#attr-text-field${attrNumber}`).focus();
  let dropdowns = document.querySelectorAll('.type');
  for (let i = 0; i < dropdowns.length; i++) {
    dropdowns[i].removeAttribute('onfocus');
    dropdowns[i].removeAttribute('onblur');
  }

  document
    .querySelector(`#dropdown${attrNumber}`)
    .setAttribute('onfocus', 'isDropdownFocused=true');
  document
    .querySelector(`#dropdown${attrNumber}`)
    .setAttribute('onblur', 'isDropdownFocused=false');
}

// export function generateAPI() {
//   var request = new XMLHttpRequest();
//   request.open('POST', '/addObjectAttributes');
//   request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
//   // form the request request json

//   // Set up iteration on each row of the table
//   var attributeList = [];
//   var attributeRows = document.querySelectorAll('.object-attribute-table > tr');
//   for (var row of attributeRows) {
//     var typeElement = row.querySelector('td > form > select');
//     var yesNoElements = row.querySelectorAll('td > form > .affirm');
//     var generationElement = row.querySelector('td > form > .generation-types');

//     // add row to json object
//     attributeList.push({
//       name: variableHandling(
//         row.querySelector('td > .attribute-name').value,
//         'var'
//       ),
//       type: typeElement.options[typeElement.selectedIndex].value,
//       description: '', //row.querySelector('td > textarea').value,
//       isUnique: false, //yesNoElements[1].checked,
//       isEncrypted: false, //yesNoElements[2].checked,
//       generationMethod: '', //generationElement.options[generationElement.selectedIndex].value,
//       isNullable: false, //yesNoElements[0].checked,
//     });
//   }

//   var jsonData = {
//     userId: localStorage['userId'],
//     objectId: localStorage['currentObjectId'],
//     attributes: attributeList,
//   };

//   console.log(jsonData);

//   request.onload = function() {
//     if (request.status >= 200 && request.status < 400) {
//       // Success!
//       var data = JSON.parse(request.responseText);
//       const attributeIds = data['attributeId'];
//       // Move to displaying the routes that just got generated
//       moveToRouteDisplay(objectId);
//     } else {
//       // We reached our target server, but it returned an error
//       alert('Enter all attribute names!');
//     }
//   };

//   request.onerror = function() {
//     // There was a connection error of some sort
//   };
//   request.send(JSON.stringify(jsonData));
// }

export function pullGeneratedRoutes(objectId) {
  var request = new XMLHttpRequest();
  request.open('POST', '/showObjectRoutes');
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  // form the request request json
  var jsonData = {
    userId: localStorage['userId'],
    objectId: objectId,
  };

  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      // Success!
      var data = JSON.parse(request.responseText);
      console.log(data);

      var routeHTML = '';
      for (var route in data['routes']) {
        routeHTML += `<div class="pure-g">
                            <h3 class="pure-u-1 route">`;
        routeHTML += '\n' + data['routes'][route] + '\n';
        routeHTML += `</h3>
                        </div>`;
      }

      document.querySelector('#generated-routes').innerHTML = routeHTML;
    } else {
      // We reached our target server, but it returned an error
    }
  };

  request.onerror = function() {
    // There was a connection error of some sort
  };

  request.send(JSON.stringify(jsonData));
}

export function moveToObjectCreation() {
  page = 'objectCreation';
  console.log('moving to object creation');
  document.querySelector('#current-route-groups').setAttribute('hidden', '');
  document.querySelector('#create-object-name-span').removeAttribute('hidden');
  document.querySelector('#object-name').focus();
}

export function moveToObjectAttributeCreation() {
  page = 'attrCreation';
  console.log('moving to object attribute creation');
  document.querySelector('#create-object-name-span').setAttribute('hidden', '');
  document
    .querySelector('#define-object-attributes-span')
    .removeAttribute('hidden');
  addAdditionalAttributeSpace();
}

export function moveToObjectAttributeCreationFromGenRoutes() {
  console.log(
    'moving back to object attribute creation after generated routes'
  );
  document.querySelector('#object-routes-view-span').setAttribute('hidden', '');
  document
    .querySelector('#define-object-attributes-span')
    .removeAttribute('hidden');
}

export function moveToRouteDisplay(objectId) {
  page = 'routeDisplay';
  pullGeneratedRoutes(objectId);
  console.log('moving to object route display / post api generation');
  document
    .querySelector('#define-object-attributes-span')
    .setAttribute('hidden', '');
  document.querySelector('#object-routes-view-span').removeAttribute('hidden');
}

export async function grabFakeUser() {
  let request = await fetch(`/grabFakeUser`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  }).catch((err) => {
    console.log('Error:', err);
    return false;
  });
  if (request.status >= 200 && request.status < 400) {
    // Success!
    var data = await request.json();
    console.log(data);

    localStorage['userId'] = data['id'];
  } else {
    // We reached our target server, but it returned an error
  }
}

export function setAPIName() {
  var request = new XMLHttpRequest();
  request.open('POST', '/setAPIName');
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  // form the request request json

  var jsonData = {
    userId: localStorage['userId'],
    apiName: document.querySelector('#api-name').value,
  };

  console.log(jsonData);

  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      var data = JSON.parse(request.responseText);
      var api_name = data['api_name'];

      document.querySelector('#api_names').innerHTML = api_name;
    } else {
      // We reached our target server, but it returned an error
    }
  };

  request.onerror = function() {
    // There was a connection error of some sort
  };

  request.send(JSON.stringify(jsonData));
}

export function generateFullAPI(serverType) {
  var request = new XMLHttpRequest();
  request.open('POST', '/generateFullAPI');
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  // form the request request json

  var jsonData = {
    userId: localStorage['userId'],
    output: serverType,
  };

  console.log(jsonData);

  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      // Success!

      var data = JSON.parse(request.responseText);
      const fileName = data.api_name + '.zip';

      let currentURL = window.location.href;
      // if currentURL has an extra '?' at the end, have to trim the end
      // else we keep the currentURL
      const currentURLlastChar = currentURL[currentURL.length - 1]; 
      const trimmedURL =
        (currentURLlastChar === '?' || currentURLlastChar === "#")
          ? currentURL.substr(0, currentURL.length - 1)
          : currentURL;
      const downloadLink = trimmedURL + 'get-compress/' + fileName;
      window.location.href = downloadLink;

      // var port_number = data['port_number'];
      // var app_uuid = data['app_uuid'];

      // document.querySelector('#port_numbers').innerHTML = port_number;
      // document.querySelector('#app_uuid').innerHTML = app_uuid;
    } else {
      // We reached our target server, but it returned an error

      //assuming error must be because an objectId has not been created yet, throwing the badParams
      alert('API must have routes created before generating!');
    }
  };

  request.onerror = function() {
    // There was a connection error of some sort
  };

  request.send(JSON.stringify(jsonData));
}

export async function validateUser() {
  let resStream = await fetch(`/isValidUser`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userId: localStorage['userId'] }),
  }).catch((err) => {
    console.log('Error:', err);
    return false;
  });
  return resStream.status === 200;
}

let page = 'landing';
export function nextPage() {
  if (page === 'landing') moveToObjectCreation();
  else if (page === 'objectCreation') addGroupRoute();
  //   else if (page === 'attrCreation') generateAPI();
  else if (page === 'routeDisplay') window.location.href = '/';
}

export function pascalCase(str) {
  // first parse through the string to separate out words, and capitalize the first letter in each found word
  return str
    .replace(/(?:^\w|[A-Z]|\b\w)/g, function(word, index) {
      return word.toUpperCase();
    })
    .replace(/\s+/g, ''); // now remove the white space
}

export function variableHandling(name, type) {
  var modified = name;

  // handle leading/trailing whitespace
  modified = modified.trim();

  // first check for illegal characters
  modified = modified.replace(/[^A-Za-z_\s0-9]/g, '');

  // now check the first character of the proposed name and add underscore if illegal
  modified = modified.replace(/^[0-9]/, '_' + modified[0]);

  // depending on the type of the variable, convert to either PascalCase or snake_case
  if (type === 'class') {
    modified = pascalCase(modified);
  } else {
    modified = modified.replace(/[\s]/g, '_');
  }

  return modified;
}

export function test2() {
  console.log('YO YOU CLICKED ME');
}

// window.onload = async function() {
//     // Don't have a login process yet. Just set the user id
//     // TODO: put login in code here instead
//     // localStorage['userId'] = 1;
//     // Add an await here
//     if(!await validateUser()){
//         await grabFakeUser();
//     }
//     console.log(localStorage['userId'])

//     // Fill in the main page with current groups for account
//     getGroups();

//     // set event listeners on flip bool buttons
//     var boolButtons = document.querySelectorAll('.bool-button');
//     for (var button of boolButtons)
//     {
//         button.addEventListener('click', flipBoolButton, false);
//     }

//     //keycode 13 is ENTER key
//     document.querySelector("body").addEventListener("keydown", e=>{
//       if (e.ctrlKey && e.keyCode === 13) nextPage();
//     })

//     //keycode 9 is TAB key
//     document.querySelector("body").addEventListener("keydown", e=>{
//       if (e.keyCode === 9 && isDropdownFocused===true && e.shiftKey===false){
//         e.preventDefault()
//         addAdditionalAttributeSpace();
//       }
//     })

//     document.querySelector('#object-name').addEventListener('keydown', function(){
//         var str = document.querySelector('#object-name').value;
//         document.querySelector('#object-name').value = str.charAt(0).toUpperCase() + str.slice(1);
//     }, false)

//     document.querySelector('#object-name-form').addEventListener('submit', function(e){
//       e.preventDefault()
//       addGroupRoute()
//     })

//     document.querySelector('#goto-define-object > .pure-button').addEventListener('click', addGroupRoute, false);

//     // add more space to add attributes button event listener
//     document.querySelector('#add-attribute-button').addEventListener('click', addAdditionalAttributeSpace, false);

//     // event listener to generate api button
//     document.querySelector('#generate-api-button').addEventListener('click', generateAPI, false);

//      // event listener to set api name button
//      document.querySelector('#set-api-name-button').addEventListener('click', setAPIName, false);

//     // event listener on edit object button on the generated routes page
//     document.querySelector('#edit-object').addEventListener('click', moveToObjectAttributeCreationFromGenRoutes, false);

//     // event listener on generate full api button
//     document.querySelector('#generate-api > button').addEventListener('click', function(){generateFullAPI("Node")}, false);
// }

let script = window.script || {};

script.request = (url, method = 'GET') => {
  // Set headers
  let headers = new Headers();

  // Return a promise
  return fetch(url, {
    method: method
  }).then(response => {
    let status = response.status,
        type   = response.headers.get("content-type");

    // Check if response is valid
    if (type && type.includes('application/json')) {
      // Return JSON
      return response.json();
    }

    throw new TypeError('Response is not JSON');
  }).catch(error => {});
}

class Allergy {
  get(id) {
    return script.request(`/api/allergies/${id}`);
  }

  // Get a overview of all ingredients
  overview() {
    return script.request(`/api/allergies`);
  }

  // Search the database for ingredients
  search(query) {
    return script.request(`/api/allergies/search/${query}`);
  }
}

script.nav = {
  open: () => {
    document.getElementById('nav').style.width = '250px';
  },
  close: () => {
    document.getElementById('nav').style.width = '0';
  }
}

script.allergies = new Allergy();

class Ingredient extends Allergy {
  get(id) {
    return script.request(`/api/ingredients/${id}`);
  }

  // Get a overview of all ingredients
  overview() {
    return script.request(`/api/ingredients`);
  }

  // Search the database for ingredients
  search(query) {
    return script.request(`/api/ingredients/search/${query}`);
  }
}

script.ingredients = new Ingredient();

class User {
  constructor() {
    this.allergy    = '/api/users/allergies/';
    this.preference = '/api/users/preferences/';
  }

  addAllergy(id) {
    console.log(`${this.allergy}${id}`)
    return script.request(`${this.allergy}${id}`, 'POST');
  }

  removeAllergy(id) {
    return script.request(`${this.allergy}${id}`, 'DELETE');
  }

  addPreference(id) {
    return script.request(`${this.preference}${id}`, 'POST');
  }

  removePreference(id) {
    return script.request(`${this.preference}${id}`, 'DELETE');
  }
}

script.user = new User();

class Roommate extends User {
  constructor() {
    super();

    let location = window.location.pathname,
        path     = location.split('/'),
        handle   = path[2],
        prefix   = `/api/roommates/${handle}`;

    this.allergy    = `/api/roommates/${handle}/allergies/`;
    this.preference = `/api/roommates/${handle}/preferences/`;
  }
}

script.roommate = new Roommate();

script.elements = (location => {
  let routes = [
    /\/roommate\/[0-9]+/,
    /\/roommate\/[0-9]+\/edit/,
    /\/diet/
  ];

  let page, controller;

  if (routes.some(route => route.test(location))) {
    if (location.match(routes[2])) {
      page = 'diet';
    } else {
      page = 'roommate';
    }

    if (page == 'diet') {
      controller = script.user;
    } else {
      controller = script.roommate;
    }

    let templateItem   = document.getElementById('template-item'),
        templateResult = document.getElementById('template-result');

    // Get the search form
    let search = document.getElementById('search');

    let results = document.getElementById('results');

    // Add a new allergy
    function add(el, type) {
      let output = document.getElementById(type);

      let href = el.href,
          id   = new URL(href).pathname.split('/')[2];

      let promise;

      if (type == 'allergies') {
        promise = controller.addAllergy(id);
      } else {
        promise = controller.addPreference(id);
      }

      promise.then(response => {
        el.parentElement.remove();

        let clone  = document.importNode(templateItem.content, true),
            link   = clone.querySelector('a'),
            button = clone.querySelector('i');

        link.href = `/allergies/${id}`;
        link.innerText = el.innerText;

        button.onclick = evt => {
          remove(button, type)
        }

        output.append(clone);

        // Remove search results
        while (results.firstChild) {
          results.removeChild(results.firstChild);
        }
      });
    }

    // Remove an allery
    function remove(el, type) {
      let parent = el.parentElement.parentElement
          href   = parent.querySelector('a').href,
          id     = new URL(href).pathname.split('/')[2];

      let promise;

      if (type == 'allergies') {
        promise = controller.removeAllergy(id);
      } else {
        promise = controller.removePreference(id);
      }

      promise.then(response => {
        parent.remove();
      });
    }

    search.onsubmit = event => {
      event.preventDefault();

      // Get search query
      let query = search.elements['search'].value;

      let value = document.querySelector('#type').value;
      let type;

      // Get search type
      if (value === 'Allergieën') {
        type = 'allergies';
      } else {
        type = 'ingredients';
      }


      // Fetch results
      script[type].search(query).then(response => {
        response.forEach(allergy => {
          console.log(allergy)
          // Import template and get nodes
          let clone  = document.importNode(templateResult.content, true),
              link   = clone.querySelector('a'),
              button = clone.querySelector('i');

              console.log(clone)

          link.href      = `/allergy/${allergy['id']}`;
          link.innerText = allergy['name'];

          button.onclick = evt => {
            add(link, type);
          };

          results.append(clone);
        });
      });
    }

    ['allergies', 'diets', 'ingredients'].forEach(type => {
      let buttons = document.querySelectorAll(`#${type} > div i`);

      buttons.forEach(el => {
        el.onclick = evt => {
          remove(el, type);
        }
      });
    })

  }
})(window.location.pathname);

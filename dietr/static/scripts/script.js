let script = window.script || {};

script.request = (url, method = 'GET') => {
  let headers = new Headers();

  return fetch(url, {
    method: method
  }).then(response => {
    let status = response.status,
        type   = response.headers.get("content-type");

    if (type && type.includes('application/json')) {
      return response.json();
    }

    throw new TypeError('Response is not JSON');
  })
  .catch(error => {});
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

script.allergy = new Allergy();

class Ingredient {
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

script.ingredient = new Ingredient();

class User {
  constructor() {
    this.allergy    = '/api/users/allergies/';
    this.preference = '/api/users/preferences/';
  }

  addAllergy(id) {
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

script.roommate = new User();

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

script.controllers = {
  roommate: document => {
    let templateRemove = document.querySelector('#template-remove'),
        templateSearch = document.querySelector('#template-search');

    (wrapper => {
      function search(query) {
        script.allergy.search(query).then(response => {
          // clear children of search outout

          for (allergy in JSON.parse(response)) {
            let clone  = document.importNode(templateRemove.content, true),
                link   = clone.querySelector('a'),
                button = clone.querySelector('.btn');

            link.href      = `/allergy/${allergy.id}`;
            link.innerText = allergy.name;

            // add event listener to button
            // append clone to search area
          }
        });
      }

      function add(el) {
        let href = el.previousElementSibling.href,
            id  = new URL(href).pathname.split('/')[2];

        script.roommate.addAllergy(id).then(response => {
          el.parentElement.remove();

          let clone  = document.importNode(templateRemove.content, true),
              link   = clone.querySelector('a'),
              button = clone.querySelector('.btn');

          link.href = `/allergies/${response.id}`;
          link.innerText = response.name;

          button.onClick(evt => {
            // remove parentElement
            // add to list of allergies
          })
        });
      }

      function del(el) {
        let href = el.previousElementSibling.href,
            id  = new URL(href).pathname.split('/')[2];

        script.roommate.removeAllergy(id).then(response => {
          el.parentElement.remove();
        });
      }
    })(document.querySelector('#allergies-wrapper'));
  }
};

script.router = ((controller, location) => {
  let routes = {
    '\/roommate\/[0-9]+\/edit': controller.roommate
  };

  for (route in routes) {
    let expression = new RegExp(route);

    if (location.match(expression)) {
      routes[route](document);
    }
  }
})(script.controllers, window.location.pathname);

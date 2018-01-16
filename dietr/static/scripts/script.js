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
  addAllergiey(id) {
    return script.request(`/api/users/allergies/${id}`, 'POST');
  }

  removeAllergiey(id) {
    return script.request(`/api/users/allergies/${id}`, 'DELETE');
  }

  addPreference(id) {
    return script.request(`/api/users/preferences/${id}`, 'POST');
  }

  removePreference(id) {
    return script.request(`/api/users/preferences/${id}`, 'DELETE');
  }
}

script.roommate = new User();

class Roommate {
  constructor() {
    let location = window.location.pathname,
        path     = location.split('/');

    this.handle = path[2];
    this.prefix = `/api/roommates/${this.handle}`;
  }

  addAllergy(id) {
    return script.request(`${this.prefix}/allergies/${id}`, 'POST');
  }

  removeAllergy(id) {
    return script.request(`${this.prefix}/allergies/${id}`, 'DELETE');
  }

  addPreference(id) {
    return script.request(`${this.prefix}/preferences/${id}`, 'POST');
  }

  removePreference(id) {
    return script.request(`${this.prefix}/preferences/${id}`, 'DELETE');
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

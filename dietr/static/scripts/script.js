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

script.allergy = new Allergy();

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

script.ingredient = new Ingredient();

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

script.controllers = {
  diet: document => {
    let templateRemove = document.querySelector('#template-remove'),
        templateAdd = document.querySelector('#template-add');

    (wrapper => {
      function search(query) {
        script.allergy.search(query).then(response => {
          // clear children of search outout
          let results = wrapper.querySelector('#allergies-search');

          response.forEach(allergy => {
            console.log(allergy)
            let clone  = document.importNode(templateAdd.content, true),
                link   = clone.querySelector('a'),
                button = clone.querySelector('.btn');

            link.href      = `/allergy/${allergy['id']}`;
            link.innerText = allergy['name'];

            button.onclick = evt => {
              add(link);
            };

            results.append(clone);
          });
        });
      }

      // Add a new allergy
      function add(el) {
        let allergies = wrapper.querySelector('#allergies');

        let href = el.href,
            id  = new URL(href).pathname.split('/')[2];

        script.user.addAllergy(id).then(response => {
          el.parentElement.remove();

          let clone  = document.importNode(templateRemove.content, true),
              link   = clone.querySelector('a'),
              button = clone.querySelector('.btn');

          link.href = `/allergies/${id}`;
          link.innerText = el.innerText;

          button.onclick = evt => {
            // remove parentElement
            // add to list of allergies
          }

          console.log(clone)
          allergies.append(clone);
        });
      }

      // Remove an allery
      function del(el) {
        let href = el.previousElementSibling.href,
            id  = new URL(href).pathname.split('/')[2];

        script.diet.removeAllergy(id).then(response => {
          el.parentElement.remove();
        });
      }

      let buttons = wrapper.querySelectorAll('a.btn');

      buttons.forEach(button => {
        console.log(button)
      })

      console.log(buttons)

      let button = wrapper.querySelector('button'),
          input  = button.previousElementSibling;

      button.onclick =evt => {
        let query = input.value;
        console.log(query)

        search(query);
      }
    })(document.querySelector('#allergies-wrapper'));
  },

  user: document => {

  }
};

script.router = ((controller, location) => {
  let routes = {
    '\/roommate\/[0-9]+': controller.roommate,
    '\/roommate\/[0-9]+\/edit': controller.roommate,
    '\/diet': controller.diet
  };

  for (route in routes) {
    let expression = new RegExp(route);

    if (location.match(expression)) {
      routes[route](document);
    }
  }
})(script.controllers, window.location.pathname);

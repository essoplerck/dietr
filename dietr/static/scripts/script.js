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

class Ingredient {
  get(id) {
    script.request(`/api/ingredients/${id}`).then(response => {
      console.log(response);
    });
  }

  // Get a overview of all ingredients
  overview() {
    script.request(`/api/ingredients`).then(response => {
      console.log(response);
    });
  }

  // Search the database for ingredients
  search(query) {
    script.request(`/api/ingredients/search/${query}`).then(response => {
      console.log(response);
    });
  }
}

script.ingredient = new Ingredient();

class Person {
  constructor() {
    this.allergies = {
      add: id => {
        url = `/api/persons/${this.handle}/allergies/${id}`;

        script.request(url, 'POST').then(response => {
          console.log(response);
        });
      }
    }

    this.ingredient = {
      add: id => {
        url = `/api/persons/${this.handle}/ingredients/${id}`

        script.request(url, 'POST').then(response => {
          console.log(response);
        });
      }
    }
  }

  get handle() {
    let location = window.location.pathname,
        path     = location.split('/');

    return path[2];
  }
}

script.person = new Person();

script.router = ((document, location) => {
  let routes = {
    '\/person\/[0-9]+\/edit': () => {
      let buttons = document.querySelectorAll('.ingredients-wrapper .btn.btn-warning')

      buttons.forEach(button => {
        console.log(button)

        let previous = button.previousElementSibling,
            path     = previous.pathname,
            id       = path.split('/')[2];

        console.log(id)

        button.addEventListener('click', event => {
          console.log('remove', id)
        });
      });
    }
  };

  for (route in routes) {
    let expression = new RegExp(route);

    if (location.match(expression)) {
      routes[route]();
    }
  }
})(document, window.location.pathname);

let script = window.script || {};

class Ingredient {
  get(id) {
    fetch(`/api/ingredients/${id}`, {
      method: 'GET'
    }).then(response => {
      let type = response.headers.get("content-type");

      if (type && type.includes('application/json')) {
        return response.json();
      }

      throw new TypeError('Response is not JSON');
    })
    .then(response => {
      console.log(response)
    })
    .catch(error => {});
  }

  // Get a overview of all ingredients
  overview() {
    fetch(`/api/ingredients`, {
      method: 'GET'
    }).then(response => {
      let type = response.headers.get("content-type");

      if (type && type.includes('application/json')) {
        return response.json();
      }

      throw new TypeError('Response is not JSON');
    })
    .then(response => {
      console.log(response)
    })
    .catch(error => {});
  }

  // Search the database for ingredients
  search(query) {
    fetch(`/api/ingredients/search/${query}`, {
      method: 'GET'
    }).then(response => {
      let type = response.headers.get("content-type");

      if (type && type.includes('application/json')) {
        return response.json();
      }

      throw new TypeError('Response is not JSON');
    })
    .then(response => {
      console.log(response)
    })
    .catch(error => {});
  }
}

script.ingredient = new Ingredient();

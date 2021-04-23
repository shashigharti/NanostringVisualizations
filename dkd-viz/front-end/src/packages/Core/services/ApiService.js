import axios from 'axios';
import { generatePath } from 'react-router';

/** @class ApiService is a parent class responsible for all the rest api calls. */
class ApiService {
  constructor(axios) {
    if (process.env.NODE_ENV == 'production') {
      // set base url for production
      this._axios = axios.create({
        baseURL: process.env.API_ENDPOINT,
      });
    } else {
      this._axios = axios;
    }
  }

  getAll(path) {
    return this._axios.get(path);
  }

  /**
   * Makes a GET api call.
   *
   * @param {string} id id of the record.
   * @param {string} path Path to the endpoint .
   * @return {Promise} Promise for the API call.
   */
  getById(id, path) {
    path = generatePath(path, { id });
    return this._axios.get(path);
  }

  getByUrl(path) {
    return this._axios.get(path);
  }

  store(path, data) {
    return this._axios.post(path, data);
  }
  post(path, data) {
    return this._axios.post(path, data);
  }

  delete(path) {
    return this._axios.delete(path);
  }

  update(path, data) {
    return this._axios.put(path, data);
  }
}

export const apiService = new ApiService(axios);

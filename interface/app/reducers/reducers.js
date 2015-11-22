import { combineReducers } from 'redux';
import * as types from '../constants/ActionTypes.js';

function products(state = [], action) {
  switch (action.type) {
    case types.RECEIVE_PRODUCTS:
      return action.products;
    default:
      return state;
  }
}

function selectedItemId(state = 0, action) {
  switch (action.type) {
    case types.SELECT_ITEM:
      return action.id;
    default:
      return state;
  }
}

function isBuyButtonEnabled(state = false, action) {
  switch (action.type) {
    case types.ENABLE_BUY_BUTTON:
      return true;
    case types.DISABLE_BUY_BUTTON:
      return false;
    default:
      return state;
  }
}

function activeCredit(state = 0, action) {
  switch (action.type) {
    case types.RECEIVE_CASH:
      return action.amount;
    default:
      return state;
  }
}

function message(state = '', action) {
  switch (action.type) {
    case types.RECEIVE_MESSAGE:
      return action.message;
    default:
      return state;
  }
}

function ccnum(state = '', action) {
  switch (action.type) {
    case types.ADD_CREDIT_CARD:
      return action.ccnum;
    default:
      return state;
  }
}

function pin(state = '', action) {
  switch (action.type) {
    case types.ADD_CARD_PIN:
      return action.pin;
    default:
      return state;
  }
}

const rootReducer = combineReducers({
  products,
  selectedItemId,
  isBuyButtonEnabled,
  activeCredit,
  message,
  ccnum,
  pin
});

export default rootReducer;

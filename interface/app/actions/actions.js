import * as types from '../constants/ActionTypes.js';
import $ from 'jquery';

export function requestProducts() {
  return {
    type: types.REQUEST_PRODUCTS,
  };
}

export function receiveProducts(json) {
  return {
    type: types.RECEIVE_PRODUCTS,
    products: json.products
  };
}

export function fetchProducts() {
  return dispatch => {
    dispatch(requestProducts());
    return $.ajax({
      url: '/api/product_list',
      dataType: 'json',
      cache: false,
      success: function (data) {
        dispatch(receiveProducts(data));
      }
    });
  }
}

export function selectItem(id) {
  return {
    type: types.SELECT_ITEM,
    id
  };
}

export function enableBuyButton() {
  return {
    type: types.ENABLE_BUY_BUTTON
  };
}

export function disableBuyButton() {
  return {
    type: types.DISABLE_BUY_BUTTON
  };
}

export function sendCash(amount) {
  return {
    type: types.SEND_CASH,
    amount
  };
}

export function receiveCash(amount) {
  return {
    type: types.RECEIVE_CASH,
    amount
  }
}

export function requestCash(amount) {
  return dispatch => {
    dispatch(sendCash(amount));
    return $.ajax({
      url: '/api/balance_refill',
      method: "POST",
      data: JSON.stringify({credit: parseFloat(amount)}),
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      success: function (data) {
        dispatch(receiveCash(Math.round(data.credit * 100) / 100));
      }
    });
  }
}

export function receiveMessage(message) {
  return {
    type: types.RECEIVE_MESSAGE,
    message
  };
}

export function buySelectedItem() {
  return {
    type: types.BUY_SELECTED_ITEM
  };
}

export function requestBuy(id, type = 'cash', paymentDetails = {}) {
  return dispatch => {
    dispatch(buySelectedItem(id));
    return $.ajax({
      url: '/api/purchase',
      method: 'POST',
      data: JSON.stringify({slot: id, payment: type, payment_details: paymentDetails}),
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      success: function (data) {
        let credit = Math.round(data.credit * 100) / 100;
        if (type == 'cash') {
          dispatch(receiveCash(Math.round(data.credit * 100) / 100));
        }
        dispatch(receiveMessage(data.result));
      }
    });
  }
}

export function addCreditCard(ccnum) {
  return {
    type: types.ADD_CREDIT_CARD,
    ccnum
  };
}

export function addCardPin(pin) {
  return {
    type: types.ADD_CARD_PIN,
    pin
  };
}

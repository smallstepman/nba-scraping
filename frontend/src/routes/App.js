import React from 'react';
import { createStore, combineReducers } from 'redux';
import { Provider } from 'react-redux';

import '../App.css';
import GamesList from '../components/GameList';
import DatePicker, {dateReducer} from '../components/DatePicker';

const INITIAL_STATE = {}
const store = createStore(combineReducers({dateReducer}), INITIAL_STATE);

export default function App() {
  return (
      <Provider store={store}>
          <DatePicker />
          <GamesList />
      </Provider>
  );
}


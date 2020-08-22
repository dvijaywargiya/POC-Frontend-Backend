import React from 'react';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import {authReducer} from "./utils/Utilities";

import Login from "./components/login";
import Home from "./components/home";
import NewRequest from "./components/newRequest"
export const AuthContext = React.createContext();
const initialState = {
  isAuthenticated: false,
  userid: null,
};

function App() {
  const [state, dispatch] = React.useReducer(authReducer, initialState);
  return (
    <AuthContext.Provider value={{state, dispatch}}>
      <Router>
        <div className="App">
          <nav className="navbar navbar-expand-lg navbar-light fixed-top">
            <div className="container">
              <Link className="navbar-brand" to={"/signIn"}>Substrate Portal</Link>
              <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
                <ul className="navbar-nav ml-auto">
                  {state.isAuthenticated ? '':
                    (
                      <li className="nav-item">
                        <Link className="nav-link" to={"/signIn"}>Login</Link>
                      </li>
                    )
                  }
                  {state.isAuthenticated ? 
                    (
                      <>
                        <li className="nav-item">
                          <Link className="nav-link" to={"/newRequest"}>New Request</Link>
                        </li>
                        <li>
                          <Link className="nav-link" to={"/"} onClick={() => {
                              dispatch({
                              type: "LOGOUT"
                            })
                          }}>Logout</Link>  
                        </li>
                      </>
                    ):''
                  }
                </ul>
              </div>
            </div>
          </nav>

          <div className="auth-wrapper">
            <div className="auth-inner">
              <Switch>
                <Route exact path='/' component={state.isAuthenticated ? Home:Login} />
                <Route path="/signIn" component={state.isAuthenticated ? Home:Login} />
                <Route path="/newRequest" component={state.isAuthenticated ? NewRequest:Login} />
              </Switch>
            </div>
          </div>
        </div>
      </Router>
    </AuthContext.Provider>
  );
}

export default App;
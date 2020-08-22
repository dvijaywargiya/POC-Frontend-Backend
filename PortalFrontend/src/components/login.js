import React from "react";
import axios from 'axios';
import { AuthContext } from "../App";

const Login = () => {
    const { dispatch } = React.useContext(AuthContext);
    const initialState = {
      username: "",
      password: "",
      isSubmitting: false,
      errorMessage: null,
      login: true
    };
    const [data, setData] = React.useState(initialState);
    const handleInputChange = event => {
        setData({
          ...data,
          [event.target.name]: event.target.value
        });
    };
    const handleFormSubmit = event => {
        event.preventDefault();
        setData({
          ...data,
          isSubmitting: true,
          errorMessage: null
        });
        axios.post("http://127.0.0.1:5000/signin", {
            username: data.username,
            password: data.password
        })
        .then(response => {
            dispatch({
                type: "LOGIN",
                payload: response.data
            })
        })
        .catch(error => {
            console.log(error.response);
            setData({
            ...data,
            isSubmitting: false,
            errorMessage: error.message || error.statusText
            });
        });
    };
    return (
        <form onSubmit={handleFormSubmit}>
            <h3>Sign In</h3>
            <div className="form-group">
                <label>Username</label>
                <input type="text" name="username" className="form-control" placeholder="Enter Username" onChange={handleInputChange}/>
            </div>
            <div className="form-group">
                <label>Password</label>
                <input type="password" name="password" className="form-control" placeholder="Enter Password" onChange={handleInputChange}/>
            </div>

            <button type="submit" className="btn btn-primary btn-block">Submit</button>
            {data.errorMessage && (
            <span className="form-error">{data.errorMessage}</span>
            )}
        </form>
    );
}

export default Login

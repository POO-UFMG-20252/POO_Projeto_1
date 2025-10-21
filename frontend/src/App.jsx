import React from 'react';
import {createBrowserRouter, RouterProvider, Route, Outlet,} from "react-router-dom"
import Register from "./pages/Register"
import Login from "./pages/Login"
import Home from "./pages/Home"
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import "./style.scss"

const Layoult = ()=>{
    return (
        <>
            <Navbar />
            <Outlet />
            <Footer />  
        </>
    );
};

const router = createBrowserRouter([
    {
        path: "/",
        element: <Layoult/>,
        children:[
            {
                path:"/",
                element:<Home/>
            }
        ]
    },
    {
        path: "/register",
        element: <Register/>,
    },
    {
        path: "/login",
        element: <Login/>,
    },
    {
        path: "/Home",
        element: <Home/>,
    },
]);

function App(){
    return (
        <div className="app">
            <div className="container">
            <RouterProvider router={router}/>
            </div>
        </div>
    );
}

export default App;
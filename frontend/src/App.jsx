import React from 'react';
import { createBrowserRouter, RouterProvider, Route, Outlet, } from "react-router-dom"
import Register from "./pages/Register"
import Login from "./pages/Login"
import Home from "./pages/Home"
import Caixa from "./pages/Caixa"
import Ponto from "./pages/Ponto"
import Pedido from "./pages/Pedido"
import Estoque from "./pages/Estoque"
import Teste from "./pages/Teste"
import Lista_Func from "./pages/Lista_Func"
import Lista_Pedidos from "./pages/Lista_Pedidos"
import Cadastro_Func from "./pages/Cadastro_Func"
import Lista_Gerente from "./pages/Lista_Gerente"
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import "./style.scss"

const Layoult = () => {
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
        element: <Layoult />,
        children: [
            {
                path: "/",
                element: <Home />
            },
            {
                path: "/caixa",
                element: <Caixa />,
            },
            {
                path: "/funcionarios",
                element: <Lista_Func />,
            },
            {
                path: "/ponto",
                element: <Ponto />,
            },
            {
                path: "/pedido",
                element: <Pedido />,
            },
            {
                path: "/estoque",
                element: <Estoque />,
            },
            {
                path: "/lista_gerente",
                element: <Lista_Gerente />,
            },
                        {
                path: "/lista_pedidos",
                element: <Lista_Pedidos />,
            },
                        {
                path: "/cadastro_func",
                element: <Cadastro_Func />,
            },
            {
                path: "/teste",
                element: <Teste />,
            }
        ]
    },
    {
        path: "/register",
        element: <Register />,
    },
    {
        path: "/login",
        element: <Login />,
    },
]);

function App() {
    return (
        <div className="app">
            <div className="container">
                <RouterProvider router={router} />
            </div>
        </div>
    );
}

export default App;
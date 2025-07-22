import { createBrowserRouter } from "react-router-dom";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage"; 

export const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginPage />, // ou seu layout se houver
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/register", // ✅ rota para registro
    element: <RegisterPage />,
  },
  // outras rotas como /register, /dashboard, etc.
]);

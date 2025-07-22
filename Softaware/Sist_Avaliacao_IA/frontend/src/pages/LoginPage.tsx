import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Eye, EyeOff } from "lucide-react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";



const schema = z.object({
  username: z.string().min(1, "Usuário obrigatório"),
  password: z.string().min(1, "Senha obrigatória"),
});

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: any) => {
    setError("");
    setLoading(true);
    try {
      const response = await axios.post("https://localhost:8001/auth/login", new URLSearchParams({
        username: data.username,
        password: data.password,
      }), {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const { access_token } = response.data;
      localStorage.setItem("token", access_token);
      navigate("/dashboard"); // Redirecionar para página após login
    } catch (err: any) {
      setError("Usuário ou senha inválidos.");
    } finally {
      setLoading(false);
    }
  };

  return (
  <div className="min-h-screen flex items-center justify-center bg-green-200">
    <Card className="w-[600px] p-6 shadow-md border bg-white">
      <CardHeader>
        <CardTitle className="text-center text-2xl font-bold">Login</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <Label htmlFor="username">Usuário</Label>
            <div className="flex items-center">
            <Input
              id="username"
              className="w-full rounded-r-none"
              {...register("username")}
            />
            {errors.username && (
              <p className="text-sm text-red-500 mt-1">
                {errors.username.message as string}
              </p>
            )}
            </div>
          </div>

          <div>
            <Label htmlFor="password">Senha</Label>
            <div className="flex items-center">
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                className="w-full rounded-r-none"
                {...register("password")}
              />
              <button
                type="button"
                className="h-full w-10 border border-l-0 border-gray-300 bg-white rounded-r-md hover:bg-gray-100 flex items-center justify-center"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            {errors.password && (
              <p className="text-sm text-red-500 mt-1">
                {errors.password.message as string}
              </p>
            )}
          </div>
          {errors.password && (
            <p className="text-sm text-red-500 mt-1">
              {errors.password.message as string}
            </p>
          )}

          {error && (
            <p className="text-sm text-red-600 text-center">{error}</p>
          )}
          <Button
            type="submit"
            className="w-full"
            disabled={loading}
          >
            {loading ? "Entrando..." : "Entrar"}
          </Button>
          <p className="text-sm text-center">
            Não tem conta?{" "}
            <a href="/register" className="text-blue-600 underline">
              Cadastre-se
            </a>
          </p>
        </form>
      </CardContent>
    </Card>
  </div>


  );
}

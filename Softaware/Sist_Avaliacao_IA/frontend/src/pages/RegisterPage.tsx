// src/pages/RegisterPage.tsx
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Button } from "../components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "../components/ui/card";

const schema = z.object({
  nome: z.string().min(1, "Nome obrigatório"),
  email: z.string().email("Email inválido"),
  username: z.string().min(3, "Usuário obrigatório"),
  password: z.string().min(6, "Senha com no mínimo 6 caracteres"),
});

type FormData = z.infer<typeof schema>;

export default function RegisterPage() {
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    setError("");
    setSuccess("");
    try {
      const response = await axios.post("https://localhost:8001/auth/register", data);
      setSuccess("Cadastro realizado com sucesso! Verifique seu e-mail.");
    } catch (err) {
      setError("Erro ao registrar. Tente novamente.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-green-200">
      <Card className="w-[600px] p-6 shadow-md border bg-white">
        <CardHeader>
          <CardTitle className="text-center text-2xl font-bold">Cadastro</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <Label htmlFor="nome">Nome completo</Label>
              <Input id="nome" {...register("nome")} />
              {errors.nome && <p className="text-sm text-red-500">{errors.nome.message}</p>}
            </div>

            <div>
              <Label htmlFor="email">E-mail</Label>
              <Input id="email" type="email" {...register("email")} />
              {errors.email && <p className="text-sm text-red-500">{errors.email.message}</p>}
            </div>

            <div>
              <Label htmlFor="username">Usuário</Label>
              <Input id="username" {...register("username")} />
              {errors.username && <p className="text-sm text-red-500">{errors.username.message}</p>}
            </div>

            <div>
              <Label htmlFor="password">Senha</Label>
              <Input id="password" type="password" {...register("password")} />
              {errors.password && <p className="text-sm text-red-500">{errors.password.message}</p>}
            </div>

            <Button type="submit" className="w-full bg-yellow-400 hover:bg-yellow-500">
              Cadastrar
            </Button>

            {error && <p className="text-red-500 text-center">{error}</p>}
            {success && <p className="text-green-600 text-center">{success}</p>}
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

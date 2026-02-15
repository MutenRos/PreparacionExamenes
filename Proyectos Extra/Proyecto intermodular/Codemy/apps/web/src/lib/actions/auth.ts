"use server"

import bcrypt from "bcryptjs"
import { prisma } from "@/lib/db/prisma"
import { signIn, signOut } from "@/lib/auth"

export async function registerUser(data: {
  name: string
  email: string
  password: string
}) {
  try {
    // Verificar si el email ya existe
    const existingUser = await prisma.user.findUnique({
      where: { email: data.email },
    })

    if (existingUser) {
      return { error: "Este email ya está registrado" }
    }

    // Hashear password
    const hashedPassword = await bcrypt.hash(data.password, 12)

    // Crear usuario
    const user = await prisma.user.create({
      data: {
        name: data.name,
        email: data.email,
        password: hashedPassword,
        role: "user",
        xp: 0,
        level: 1,
        streak: 0,
      },
    })

    return { success: true, userId: user.id }
  } catch (error) {
    console.error("Error registering user:", error)
    return { error: "Error al crear la cuenta" }
  }
}

export async function loginWithCredentials(email: string, password: string) {
  try {
    const result = await signIn("credentials", {
      email,
      password,
      redirect: false,
    })
    
    return { success: true }
  } catch (error: any) {
    return { error: error.message || "Credenciales inválidas" }
  }
}

export async function logoutUser() {
  await signOut({ redirect: false })
  return { success: true }
}

export async function getUserProfile(userId: string) {
  try {
    const user = await prisma.user.findUnique({
      where: { id: userId },
      select: {
        id: true,
        name: true,
        email: true,
        image: true,
        role: true,
        xp: true,
        level: true,
        streak: true,
        subscriptionTier: true,
        createdAt: true,
      },
    })
    return user
  } catch (error) {
    return null
  }
}

export async function updateUserXP(userId: string, xpToAdd: number) {
  try {
    const user = await prisma.user.findUnique({
      where: { id: userId },
    })

    if (!user) return null

    const newXP = user.xp + xpToAdd
    const newLevel = Math.floor(newXP / 1000) + 1 // 1000 XP por nivel

    const updated = await prisma.user.update({
      where: { id: userId },
      data: {
        xp: newXP,
        level: newLevel,
        lastActiveAt: new Date(),
      },
    })

    return { xp: updated.xp, level: updated.level }
  } catch (error) {
    return null
  }
}

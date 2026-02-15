import { createClient as createSupabaseClient, SupabaseClient } from '@supabase/supabase-js'
import type { Database } from './database.types'

// Helper para obtener variables de entorno (lazy, solo cuando se necesitan)
function getEnvVar(key: string): string {
  if (typeof process !== 'undefined' && process.env) {
    return process.env[key] || ''
  }
  return ''
}

// Crear cliente de Supabase
export function createClient() {
  const supabaseUrl = getEnvVar('NEXT_PUBLIC_SUPABASE_URL')
  const supabaseAnonKey = getEnvVar('NEXT_PUBLIC_SUPABASE_ANON_KEY')
  
  if (!supabaseUrl || !supabaseAnonKey) {
    console.warn('Supabase credentials not configured. Please check your .env.local file.')
    // Retornar un cliente dummy para evitar crashes
    return createSupabaseClient<Database>(
      'https://placeholder.supabase.co',
      'placeholder-key',
      { auth: { autoRefreshToken: false, persistSession: false } }
    )
  }
  
  return createSupabaseClient<Database>(supabaseUrl, supabaseAnonKey, {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true
    },
    realtime: {
      params: {
        eventsPerSecond: 10
      }
    }
  })
}

// Cliente público de Supabase (lazy initialization)
let _supabase: SupabaseClient<Database> | null = null
export const supabase = new Proxy({} as SupabaseClient<Database>, {
  get(target, prop) {
    if (!_supabase) {
      _supabase = createClient()
    }
    return (_supabase as any)[prop]
  }
})

// Cliente con service role (para operaciones admin)
export function createAdminClient() {
  const supabaseUrl = getEnvVar('NEXT_PUBLIC_SUPABASE_URL')
  const serviceRoleKey = getEnvVar('SUPABASE_SERVICE_ROLE_KEY')
  
  if (!supabaseUrl || !serviceRoleKey) {
    console.warn('Supabase admin credentials not configured.')
    return createSupabaseClient<Database>(
      'https://placeholder.supabase.co',
      'placeholder-key',
      { auth: { autoRefreshToken: false, persistSession: false } }
    )
  }
  
  return createSupabaseClient<Database>(
    supabaseUrl,
    serviceRoleKey,
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false
      }
    }
  )
}

// Cliente admin (lazy initialization)
let _supabaseAdmin: SupabaseClient<Database> | null = null
export const supabaseAdmin = new Proxy({} as SupabaseClient<Database>, {
  get(target, prop) {
    if (!_supabaseAdmin) {
      _supabaseAdmin = createAdminClient()
    }
    return (_supabaseAdmin as any)[prop]
  }
})

// Helper para obtener el usuario actual
export async function getCurrentUser() {
  const { data: { user }, error } = await supabase.auth.getUser()
  if (error) throw error
  return user
}

// Helper para obtener el perfil del usuario
export async function getUserProfile(userId?: string) {
  const id = userId || (await getCurrentUser())?.id
  if (!id) throw new Error('No user found')
  
  const { data, error } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', id)
    .single()
  
  if (error) throw error
  return data
}

// Helper para crear/actualizar perfil
export async function upsertProfile(profile: Partial<Database['public']['Tables']['profiles']['Insert']>) {
  const { data, error } = await (supabase
    .from('profiles') as any)
    .upsert(profile)
    .select()
    .single()
  
  if (error) throw error
  return data
}

// Helpers para conceptos y currículo
export async function getConcepts(filters?: {
  track?: string
  level?: number
  language?: string
}) {
  let query = supabase.from('concepts').select(`
    *,
    concept_bindings!inner(*)
  `)
  
  if (filters?.track) {
    query = query.eq('track', filters.track)
  }
  
  if (filters?.level !== undefined) {
    query = query.eq('level', filters.level)
  }
  
  if (filters?.language) {
    query = query.eq('concept_bindings.language', filters.language)
  }
  
  const { data, error } = await query
  if (error) throw error
  return data
}

// Helpers para progreso
export async function getUserProgress(userId?: string) {
  const id = userId || (await getCurrentUser())?.id
  if (!id) throw new Error('No user found')
  
  const { data, error } = await supabase
    .from('concept_progress')
    .select(`
      *,
      concepts(*)
    `)
    .eq('user_id', id)
  
  if (error) throw error
  return data
}

// Helper para actualizar progreso
export async function updateProgress(
  conceptId: string,
  language: string,
  updates: Partial<Database['public']['Tables']['concept_progress']['Update']>
) {
  const userId = (await getCurrentUser())?.id
  if (!userId) throw new Error('No user found')
  
  const { data, error} = await (supabase
    .from('concept_progress') as any)
    .upsert({
      user_id: userId,
      concept_id: conceptId,
      language,
      ...updates,
      last_activity_at: new Date().toISOString()
    })
    .select()
    .single()
  
  if (error) throw error
  return data
}

// Helpers para ejercicios
export async function getExercisesByConceptId(conceptId: string, language?: string) {
  let query = supabase
    .from('exercises')
    .select(`
      *,
      exercise_bindings(*)
    `)
    .eq('concept_id', conceptId)
  
  if (language) {
    query = query.eq('exercise_bindings.language', language)
  }
  
  const { data, error } = await query
  if (error) throw error
  return data
}

// Helper para crear envío
export async function createSubmission(submission: Database['public']['Tables']['submissions']['Insert']) {
  const { data, error } = await (supabase
    .from('submissions') as any)
    .insert(submission)
    .select()
    .single()
  
  if (error) throw error
  return data
}

// Helper para obtener envíos del usuario
export async function getUserSubmissions(userId?: string, exerciseId?: string) {
  const id = userId || (await getCurrentUser())?.id
  if (!id) throw new Error('No user found')
  
  let query = supabase
    .from('submissions')
    .select(`
      *,
      exercises(*)
    `)
    .eq('user_id', id)
    .order('created_at', { ascending: false })
  
  if (exerciseId) {
    query = query.eq('exercise_id', exerciseId)
  }
  
  const { data, error } = await query
  if (error) throw error
  return data
}

// Helpers para gamificación
export async function getUserXP(userId?: string) {
  const id = userId || (await getCurrentUser())?.id
  if (!id) throw new Error('No user found')
  
  const { data, error } = await supabase
    .from('user_xp')
    .select('*')
    .eq('user_id', id)
    .single()
  
  if (error && error.code !== 'PGRST116') throw error // PGRST116 = no rows
  return data || {
    user_id: id,
    total_xp: 0,
    level: 1,
    xp_in_level: 0,
    streak_days: 0,
    longest_streak: 0
  }
}

// Helper para añadir XP
export async function addXP(points: number, reason: string) {
  const userId = (await getCurrentUser())?.id
  if (!userId) throw new Error('No user found')
  
  // Obtener XP actual
  const currentXP = await getUserXP(userId)
  
  // Calcular nuevo XP y nivel
  const newTotalXP = currentXP.total_xp + points
  const newLevel = Math.floor(newTotalXP / 1000) + 1 // 1000 XP por nivel
  const newXPInLevel = newTotalXP % 1000
  
  // Actualizar XP
  const { data, error } = await (supabase
    .from('user_xp') as any)
    .upsert({
      user_id: userId,
      total_xp: newTotalXP,
      level: newLevel,
      xp_in_level: newXPInLevel,
      updated_at: new Date().toISOString()
    })
    .select()
    .single()
  
  if (error) throw error
  
  // Registrar evento
  await (supabase.from('user_events') as any).insert({
    user_id: userId,
    event_type: 'xp_earned',
    event_data: { points, reason, new_total: newTotalXP }
  })
  
  return data
}

// Helper para badges del usuario
export async function getUserBadges(userId?: string) {
  const id = userId || (await getCurrentUser())?.id
  if (!id) throw new Error('No user found')
  
  const { data, error } = await supabase
    .from('user_badges')
    .select(`
      *,
      badges(*)
    `)
    .eq('user_id', id)
    .order('earned_at', { ascending: false })
  
  if (error) throw error
  return data
}

// Types para TypeScript
export type SupabaseClientType = SupabaseClient<Database>
export type Tables = Database['public']['Tables']
export type Enums = Database['public']['Enums']
export interface League {
  id: number
  name: string
  slug: string
  logo: string | null
  image: string | null
}

export interface Collection {
  id: number
  name: string
  slug: string
  image: string | null
}

export interface Category {
  id: number
  name: string
  slug: string
  parent: number | null
  league: number | null
  collection: number | null
}

export interface Patch {
  id: number
  name: string
  image: string | null
  extra_price: string
}

export interface SizeChart {
  id: number
  name: string
  image: string
  description: string
}

export interface ProductImage {
  id: number
  image: string
  alt_text: string
  is_primary: boolean
  sort_order: number
}

export interface ProductList {
  id: number
  name: string
  slug: string
  price: string
  original_price: string | null
  discount_percentage: number
  primary_image: string | null
  league_name: string | null
  category_name: string | null
  is_featured: boolean
}

export interface ProductDetail {
  id: number
  name: string
  slug: string
  description: string
  price: string
  original_price: string | null
  discount_percentage: number
  available_sizes: string[]
  allow_name_customization: boolean
  allow_number_customization: boolean
  images: ProductImage[]
  patches: Patch[]
  size_chart: SizeChart | null
  league: League | null
  category: Category | null
  stock: number
}

export interface CartItem {
  id: number
  product: ProductList
  size: string
  custom_name: string
  custom_number: string
  patch: Patch | null
  quantity: number
  subtotal: string
}

export interface Cart {
  items: CartItem[]
  total: string
  count: number
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// ── Auth ──────────────────────────────────────────────────────────
export interface AuthUser {
  id: number
  email: string
  first_name: string
  last_name: string
  full_name: string
  phone: string
  address_line1: string
  address_line2: string
  city: string
  postal_code: string
  country: string
  date_joined: string
  is_staff: boolean
}

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  first_name: string
  last_name: string
  password: string
  password_confirm: string
}

export interface AuthResponse {
  user: AuthUser
  access_token: string
}

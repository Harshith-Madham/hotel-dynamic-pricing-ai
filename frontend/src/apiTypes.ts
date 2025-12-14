export type Hotel = {
  id: number;
  name: string;
  city: string;
  country: string;
};

export type RoomType = {
  id: number;
  hotel_id: number;
  name: string;
  capacity: number;
  base_price: number;
};

export type PriceRecommendationRequest = {
  hotel_id: number;
  room_type_id: number;
  check_in_date: string; // "YYYY-MM-DD"
  stay_length: number;
  booking_window: number;
};

export type PriceRecommendationResponse = {
  hotel_id: number;
  room_type_id: number;
  check_in_date: string;
  recommended_price: number;
  model_price: number;
  base_price: number;
  currency: string;
};

import axios from "axios";
import type {
  Hotel,
  RoomType,
  PriceRecommendationRequest,
  PriceRecommendationResponse,
} from "./apiTypes";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export async function fetchHotels(): Promise<Hotel[]> {
  const res = await api.get<Hotel[]>("/hotels");
  return res.data;
}

export async function fetchRoomTypesForHotel(hotelId: number): Promise<RoomType[]> {
  const res = await api.get<RoomType[]>(`/hotels/${hotelId}/room-types`);
  return res.data;
}

export async function fetchPriceRecommendation(
  payload: PriceRecommendationRequest
): Promise<PriceRecommendationResponse> {
  const res = await api.post<PriceRecommendationResponse>(
    "/price-recommendation",
    payload
  );
  return res.data;
}

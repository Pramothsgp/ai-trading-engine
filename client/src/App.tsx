// src/App.tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "./components/layout";
import Dashboard from "./pages/dashboard";
import BacktestPage from "./pages/backtest";
import WalkforwardPage from "./pages/walkforward";
import StrategiesPage from "./pages/strategies";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/backtest" element={<BacktestPage />} />
          <Route path="/walkforward" element={<WalkforwardPage />} />
          <Route path="/strategies" element={<StrategiesPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

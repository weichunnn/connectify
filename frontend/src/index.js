import "@fontsource/raleway/400.css";

import React, { StrictMode } from "react";
import * as ReactDOM from "react-dom/client";

import { ChakraProvider, ColorModeScript } from "@chakra-ui/react";

import theme from "./theme";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Feed from "./pages/Feed";
import Recommend from "./pages/Recommend";
import Landing from "./pages/Landing";

const container = document.getElementById("root");
const root = ReactDOM.createRoot(container);

root.render(
  <ChakraProvider theme={theme}>
    <ColorModeScript initialColorMode={theme.config.initialColorMode} />
    <StrictMode>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="feed" element={<Feed />} />
          <Route path="recommend" element={<Recommend />} />
        </Routes>
      </BrowserRouter>
    </StrictMode>
  </ChakraProvider>
);

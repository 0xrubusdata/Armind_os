"use client";

import { useEffect, useState } from "react";
import checkData from "../../utils/checkData";
import Header from "./Header";
import Footer from "./Footer";
import Main from "./Main";
import PopupSettings from "../organisms/PopupSettings";

const Layout = ({ children }: { children: React.ReactNode }) => {
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    const verifyData = async () => {
      const isConfigured = await checkData();
      setShowPopup(!isConfigured);
    };
    verifyData();
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <Main>{children}</Main>
      <Footer />
      {showPopup && <PopupSettings />} {/* Affiche le popup si les données sont incomplètes */}
    </div>
  );
};

export default Layout;

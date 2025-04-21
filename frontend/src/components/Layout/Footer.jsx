import React from "react";
import { FaFacebookF, FaTwitter, FaInstagram, FaLinkedinIn } from "react-icons/fa";

const Footer = () => {
    return (
        <footer className="bg-gradient-to-r from-green-700 to-green-500 text-white py-6 mt-16">
            <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center">
                {/* Logo & Text */}
                <div className="text-center md:text-left">
                    <h2 className="text-2xl font-extrabold tracking-wide">SustainaWare</h2>
                    <p className="text-sm text-green-200 mt-2">
                        Empowering sustainability through technology.
                    </p>
                </div>

                {/* Social Icons */}
                <div className="flex space-x-4 mt-4 md:mt-0">
                    {[FaFacebookF, FaTwitter, FaInstagram, FaLinkedinIn].map((Icon, index) => (
                        <a
                            key={index}
                            href="#"
                            className="text-white text-xl p-2 rounded-full bg-green-600 hover:bg-green-800 transition duration-300"
                        >
                            <Icon />
                        </a>
                    ))}
                </div>
            </div>

            {/* Copyright */}
            <div className="text-center text-sm text-green-200 mt-4 border-t border-green-400 pt-4">
                &copy; {new Date().getFullYear()} SustainaWare. All rights reserved.
            </div>
        </footer>
    );
};

export default Footer;

import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "../context/AuthContext";
import chatbotGif from "../assets/waste-management.gif";
import FeedbackList from "../components/Feedback/FeedbackList";
import { useState } from "react";

const Home = () => {
    const { user } = useAuth();
    const [isModalOpen, setIsModalOpen] = useState(false);

    return (
        <div
            className={`${user ? "min-h-screen" : "min-h-[80vh]"} flex flex-col items-center px-6 md:px-12 pt-24 pb-16 transition-all`}
        >
            {/* Hero Section */}
            <div className="flex flex-col md:flex-row items-center justify-between max-w-6xl w-full gap-10">
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 1 }}
                    className="text-center md:text-left max-w-lg"
                >
                    <h1 className="text-5xl md:text-6xl font-extrabold leading-tight">
                        Empowering <span className="text-green-600">Sustainability</span> with AI
                    </h1>
                    <p className="text-gray-400 text-lg mt-4">
                        Use AI to classify waste, make smarter recycling decisions, and contribute to a greener future.
                    </p>

                    {/* Buttons */}
                    <div className="mt-10 flex flex-wrap items-center gap-6">
                        {/* Get Started / Ask a Question Button */}
                        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                            <Link
                                to={user ? "/chatbot" : "/register"}
                                className="bg-green-600 text-white px-8 py-3 rounded-full shadow-md text-lg font-semibold hover:bg-green-700 transition-all"
                            >
                                {user ? "Ask a Question" : "Get Started"}
                            </Link>
                        </motion.div>

                        {/* Watch Demo Button */}
                        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                            <button
                                onClick={() => setIsModalOpen(true)}
                                className="bg-black text-white px-8 py-3 rounded-full shadow-md text-lg font-semibold hover:bg-gray-900 transition-all cursor-pointer"
                            >
                                Watch Demo
                            </button>
                        </motion.div>
                    </div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 1 }}
                    className="w-full md:w-[500px] flex justify-center"
                >
                    <img src={chatbotGif} alt="Chatbot Demo" className="w-full" />
                </motion.div>
            </div>

            {/* Feedback Section - Only visible when user is logged in */}
            {user && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1 }}
                    className="mt-16 w-full max-w-6xl text-center px-4"
                >
                    <h2 className="text-3xl font-bold text-green-600">Users Feedback 💬</h2>
                    <p className="text-gray-500 text-lg mt-2">See what others are saying about our platform.</p>
                    <FeedbackList userId={user.id} isAllFeedback={true} />
                </motion.div>
            )}

            {/* Demo Video Modal */}
            {isModalOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg shadow-lg p-6 max-w-3xl w-full relative">
                        <button onClick={() => setIsModalOpen(false)} className="absolute top-3 right-3 text-gray-600 hover:text-gray-900 text-2xl">&times;</button>
                        <h2 className="text-xl font-bold mb-4">Demo Video</h2>
                        <div className="relative w-full h-0 pb-[56.25%]">
                            <iframe
                                className="absolute top-0 left-0 w-full h-full"
                                src="https://www.youtube.com/embed/YOUR_VIDEO_ID"
                                title="Demo Video"
                                frameBorder="0"
                                allowFullScreen
                            ></iframe>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Home;

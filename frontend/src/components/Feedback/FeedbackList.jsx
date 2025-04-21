import React from "react";
import { useEffect, useState } from "react";
import { getFeedbacks } from "../../api/feedback";
import { Loader2, User } from "lucide-react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const FeedbackList = React.memo(({ userId, isAllFeedback = false }) => {
    const [feedbacks, setFeedbacks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchFeedbacks = async () => {
            try {
                const data = await getFeedbacks(userId, isAllFeedback);
                console.log("Fetched Feedbacks from API:", data); 

                // Filter out duplicates
                const uniqueFeedbacks = data.filter((value, index, self) =>
                    index === self.findIndex((t) => t.id === value.id)
                );
                setFeedbacks(uniqueFeedbacks);
            } catch (err) {
                setError("Failed to fetch feedback.");
                setFeedbacks([]);
            }
            setLoading(false);
        };
        fetchFeedbacks();
    }, [userId, isAllFeedback]); 

    const sliderSettings = {
        dots: true,
        infinite: true,
        speed: 1000,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        arrows: false,
    };

    return (
        <div className="w-full max-w-4xl mx-auto mt-2 p-8 bg-white rounded-2xl">
            {loading ? (
                <div className="flex justify-center py-8">
                    <Loader2 className="animate-spin text-gray-500" size={40} />
                </div>
            ) : error ? (
                <p className="text-red-500 text-center">{error}</p>
            ) : feedbacks.length === 0 ? (
                <p className="text-gray-500 text-center">No feedback available.</p>
            ) : (
                <Slider {...sliderSettings}>
                    {feedbacks.map((feedback) => (
                        <div key={feedback.id} className="p-6 bg-gray-50 rounded-xl text-center">
                            <div className="flex flex-col items-center space-y-3">
                                <User className="text-gray-700" size={40} />
                                <p className="text-xl font-semibold text-gray-800">{feedback.user_name || "Anonymous"}</p>
                                <p className="text-gray-700 text-lg italic">"{feedback.feedback_text || "No feedback provided."}"</p>
                                <span className="text-yellow-500 font-semibold text-xl">{feedback.rating}⭐</span>
                            </div>
                        </div>
                    ))}
                </Slider>
            )}
        </div>
    );
});

export default FeedbackList;

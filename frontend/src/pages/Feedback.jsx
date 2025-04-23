import FeedbackForm from "../components/Feedback/FeedbackForm";
import FeedbackList from "../components/Feedback/FeedbackList";

const Feedback = () => {
    return (
        <div className="container mx-auto p-6 space-y-6">
            <FeedbackForm />
            <FeedbackList />
        </div>
    );
};

export default Feedback;
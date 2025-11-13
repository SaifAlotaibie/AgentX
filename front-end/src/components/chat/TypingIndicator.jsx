import { motion } from 'framer-motion';

const TypingIndicator = () => {
  return (
    <div className="flex items-center gap-2 px-4 py-3 bg-white rounded-2xl shadow-sm max-w-[80px]">
      {[0, 1, 2].map((index) => (
        <motion.div
          key={index}
          className="w-2 h-2 bg-qiwa-primary rounded-full"
          animate={{
            y: [0, -8, 0],
          }}
          transition={{
            duration: 0.6,
            repeat: Infinity,
            delay: index * 0.1,
          }}
        />
      ))}
    </div>
  );
};

export default TypingIndicator;


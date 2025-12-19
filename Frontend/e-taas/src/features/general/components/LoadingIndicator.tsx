
type CircularLoaderProps = {
  size?: number;
  strokeWidth?: number;
};


export const LoadingIndicator: React.FC<CircularLoaderProps> = ({
  size = 40,
  strokeWidth = 4
}) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 50 50"
      className="animate-spin"
    >
      <circle
        cx="25"
        cy="25"
        r="20"
        fill="none"
        stroke="currentColor"
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeDasharray="31.4 31.4"
        className="text-pink-500"
      />
    </svg>
  );
}
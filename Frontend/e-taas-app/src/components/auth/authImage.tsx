import eTaas from "../../assets/etaas.png";

const authImage = () => {
  return (
      <>
        <div className="hidden lg:flex lg:w-3/5 items-center justify-center p-8">
        <div className="w-full max-w-4x h-189 rounded-2xl flex items-center bg-white shadow-lg justify-center">
          <img 
            src={eTaas} 
            alt="eTaas Logo" 
            className="w-full h-full object-full rounded-2xl"
          />
        </div>
      </div>
      </>
    )
}

export default authImage
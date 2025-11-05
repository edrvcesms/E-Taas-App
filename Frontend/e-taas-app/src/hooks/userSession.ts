import { useAuth } from "../context/AuthContext";
import { useEffect } from "react";
import { getUserDetails } from "../services/user/UserDetails";
import { useQuery } from "@tanstack/react-query";

export const useUserSession = () => {
  const { setIsAuthenticated, setUser, setIsLoading } = useAuth();
  
  const { data: userDetails, isLoading: queryLoading } = useQuery({
      queryKey: ['userDetails'],
      queryFn: async () => {
        const details = await getUserDetails();
        return details;
      },
      retry: false,
      refetchOnWindowFocus: false,
    });

    useEffect(() => {
      setIsLoading(queryLoading);
    }, [queryLoading]);

    useEffect(() => {
      if (userDetails) {
        setUser(userDetails);
        setIsAuthenticated(true);
      } else {
        setUser(null);
        setIsAuthenticated(false);
      }
    }, [userDetails]);

  // useEffect (() => {
  //   const checkUserSession = async () => {
  //     setIsLoading(true);
  //     try {
  //       const userDetails =  await getUserDetails();
  //       if (userDetails) {
  //         setUser(userDetails);
  //         setIsAuthenticated(true);
  //       } else {
  //         setIsAuthenticated(false);
  //         setUser(null);
  //       }
  //     } catch (error) {
  //       console.error("Error checking user session:", error);
  //       setIsAuthenticated(false);
  //     } finally {
  //       setIsLoading(false);
  //     }
  //   }
  //   checkUserSession();
  // }, [])
}
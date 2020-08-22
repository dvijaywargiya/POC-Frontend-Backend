import React, {useState, useEffect} from "react";
import { AuthContext } from "../App";
import axios from 'axios';

const Home = () => {
    const { state } = React.useContext(AuthContext);
    const [userMetrics, setUserMetrics] = useState([]);
    const [favoriteDatsets, setFavoriteDatasets] = useState([])
    useEffect(() => {
        const fetchRequests = async () => {
          const response = await axios.post("http://127.0.0.1:5000/getUserMetrics", {
              userid: state.userid,
          });
          let tempVar = response.data
          setUserMetrics(tempVar);
          let datasetsObj = JSON.parse(tempVar.datasetExtracted)
          let tempList = []
          for (var k in datasetsObj){
              if (datasetsObj[k] >= 2)
                tempList.push(k)
          }
          setFavoriteDatasets(tempList)
        }
        fetchRequests();
      }, [state.userid]);
    return (
        <div>
            <h1> Hello {state.userid}</h1>
            {userMetrics === null && <p>Loading User Metrics...</p>}
            {
                userMetrics === null ? '': (
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Number of Requests</th>
                            <th>Successful Transactions</th>
                            <th>Reliability</th>
                            <th>Favorite Dataset(s)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{userMetrics.totalExtractions}</td>
                            <td>{userMetrics.successfulExtractions}</td>
                            <td>{(userMetrics.totalExtractions > 0) ? (userMetrics.successfulExtractions/userMetrics.totalExtractions)*100: 0 }%</td>
                            <td>
                                {
                                    favoriteDatsets.map((dataset) => (
                                        dataset + ", "
                                    ))
                                }
                            </td>
                        </tr>
                    </tbody>
                </table>
                )
            }
        </div>
    );
}

export default Home
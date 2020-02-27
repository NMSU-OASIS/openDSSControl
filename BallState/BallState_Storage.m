clear
clc

%[DSSStartOK, DSSObj, DSSText] = DSSStartup;
DSSObj = actxserver('OpenDSSEngine.DSS');
DSSText = DSSObj.Text;

%if DSSStartOK
    % Compile the circuit master file for the first time
    myDir = 'C:\Users\thexpendable\Documents\OpenDSS\Battery\openDSSControl-master\BallState_Battery';
     
      % Set up the interface variables
      DSSText.Command = ['Compile (',myDir,'\Ball_State_CircuitRW.dss)'];
      DSSCircuit=DSSObj.ActiveCircuit;
      DSSSolution=DSSCircuit.Solution;
      
      %Get an an initial solve of the circuit to verify that everything is
      %set up correctly
      DSSCircuit.Solution.Solve;
     
      
      %%% Some DSS commands to set the solution mode, time step, and number
      %%% of time-steps executed per solve command
      DSSText.Command = 'set mode=yearly';
      DSSCircuit.Solution.Number=1;
      DSSSolution.MaxControlIterations=40000;
      DSSCircuit.Solution.Stepsize = 900; % Timestep Defined in Seconds
      DSSText.command = 'set controlmode=static';
      
      
     present_step=2;  % Counter to keep track of time steps
     TSinterval=35040;  % Solution interval of time-steps
     num_pts=TSinterval; % Solve counter for solution interval
     Stor_iter=1;  % counter for the Storage iterations

   
    % Pre-alocate empty arrays for storing power and voltage
     totalP=zeros(num_pts,1);
%     totalQ=zeros(num_pts,1);
     StorP=zeros(num_pts,1);
%     StorQ=zeros(num_pts,1);
%     Sub_V1=zeros(num_pts,1);
    Stor_V1=zeros(num_pts,1);
    New_V1=zeros(num_pts,1);
    New_P=zeros(num_pts,1);
    %pf=zeros(num_pts,1)
    Volt_Event=zeros(num_pts,1);  %Blank array to track voltage override events
    P_Event=zeros(num_pts,1);
    
    %Some constants
    Target_PF=0.98;  % Target power factor for feeder head 
    Th_Pr=cosd(Target_PF);  % Target angle for power quality at feeder head
    Stor_V_Base=12470;
    StorON=1.1;  %Setting for Charging the storage if the Stor_V1 is > StorON*Stor_V_Base
    StorOFF=0.8;  %Setting for Discharging the storage if the Stor_V1 is < StorOFF*Stor_V_Base
      
    
    % Set the PCS mode name for case and file naming
    PCSMode='BallState';

    
        disp(['Scenario=',PCSMode]);

%%% Demand Interval Commands 
        %DSSText.command = 'Set overloadreport=true';
        %DSSText.command = 'set voltexceptionreport=true';
        %DSSText.command = 'set DemandInterval=TRUE';
        %DSSText.command = 'set DIVerbose=TRUE';
       
        
  %%% Code to execute the storage controller for PF mode 
        %DSSText.command = 'New StorageController.Battery_Ctrl element=Line.227_1505791_2 1 modeCharge=Time TimeChargeTrigger=2  ModeDischarge=PeakShave kWTarget=5300 PFBand=2 eventLog=yes VarDispatch=yes InhibitTime=0 %RateCharge=50';
        %DSSText.command = 'edit StorageController.Battery enabled=false';
        %DSSText.command = 'edit StorageController.Battery enabled=true';
        
    while present_step<=num_pts
         
         DSSCircuit.Solution.Solve;  % Execute a solution of the present time step (each time this is executed the time advances to the next time step)
         
         
           ActiveElement=DSSCircuit.SetActiveElement('Line.L1');
            V{1,1}=DSSCircuit.ActiveElement.VoltagesMagAng;
            v=V{1,1};
            Stor_V1(present_step)=v(1)*3^0.5;
            S{1,1}=DSSCircuit.ActiveElement.Powers;
            sp=S{1,1};
            StorP(present_step)=sp(1);
            
                            %P{1,1}=DSSCircuit.ActiveElement.powers;
                            %B=P{1};
                            %totalP(present_step)=B(1)+B(3)+B(5);  %Total Real power at the present step
                            % % %totalQ(present_step)=(B(2)+B(4)+B(6));  % Total Reactive power at the present step
                            % % %Target_Q=-1*totalP(present_step)*tand(Th_Pr);  %Target var to achieve the leading power factor setting
                            % % %Req_Q=-1*(Target_Q-totalQ(present_step));%net var required from the capacitor to achieve the target var
                            % % %pf(present_step)=cosd(atand(totalQ(present_step)/totalP(present_step)));
                            Hr=DSSSolution.Hour;
                            
                            
       %%Storage Decision: Revert to idling
            %if present_step>=2 && Volt_Event(present_step-1)~=0
            if present_step>=2 && P_Event(present_step-1)~=0
                   %The Default state for the storage system is idling, but
                   %if switching to idling will cause the voltage to change
                   %to a point where it needs to be switched on/off again
                   %the storage will not revert to idling and will remain
                   %in its current state of charge/discharge
    
                           DSSText.Command = 'edit Storage.Battery  kW=1000.0  kWrated=1500.0 kVa=1000 kVAR=1000 state=idling enabled=yes';  %Recalculate the Voltage after switching Storage ON/OFF to determine if change worked
                           DSSSolution.SolveNoControl  % Do a solve without advancing the time-step
                           ActiveElement=DSSCircuit.SetActiveElement('Line.L1');
                           V{1,1}=DSSCircuit.ActiveElement.VoltagesMagAng;
                           v=V{1,1};
                           New_V1(present_step)=v(1)*3^0.5;
                           S{1,1}=DSSCircuit.ActiveElement.Powers;
                           sp=S{1,1};
                           New_P(present_step)=sp(1);
                            
                            %if New_V1(present_step)>StorON*Stor_V_Base && Volt_Event(present_step-1)==1
                            if New_P(present_step)<=650 && P_Event(present_step-1)==1
                               DSSText.Command = 'edit Storage.Battery  kW=1.0  kWrated=1500.0 kVa=1000 kVAR=1000 state=Charging enabled=yes';
                               P_Event(present_step)=1;
                               %Volt_Event(present_step)=1;

                            %elseif New_V1(present_step)<StorOFF*Stor_V_Base && Volt_Event(present_step-1)==-1
                            elseif New_P(present_step)>=750 && P_Event(present_step-1)==-1
                                DSSText.Command = 'edit Storage.Battery  kW=1.0  kWrated=1500.0 kVa=1000 kVAR=-1000 state=Discharging enabled=yes';
                                P_Event(present_step)=-1;
                                %Volt_Event(present_step)=-1;
                            else
                                P_Event(present_step)=0;
                                %Volt_Event(present_step)=0;
                            end 
                   
             end
       
       
            
       %%Storage Decision: Charge/Discharge
                 %%StorON*Stor_V_Base
            %if Stor_V1(present_step)>StorON*Stor_V_Base && strcmp(PCSMode,'BallState')==1 && Volt_Event(present_step-1)~=1
            if StorP(present_step)<=650 && strcmp(PCSMode,'BallState')==1 && P_Event(present_step-1)~=1
                 DSSText.Command = 'edit Storage.Battery  kW=1.0  kWrated=1500.0 kVa=1000 kVAR=1000 state=Charging enabled=yes';
                 %DSSText.Command = 'Storage.Battery.state=Charging';
                  disp('Overvoltage Event')
                  disp(Hr)
                  P_Event(present_step)=1;
                  %Volt_Event(present_step)=1;
            %elseif  Stor_V1(present_step)<StorOFF*Stor_V_Base  && strcmp(PCSMode,'BallState')==1 && Volt_Event(present_step-1)~=-1
            elseif  StorP(present_step)>=750  && strcmp(PCSMode,'BallState')==1 && P_Event(present_step-1)~=-1
                   DSSText.Command = 'edit Storage.Battery  kW=1.0  kWrated=1500.0 kVa=1000 kVAR=-1000 state=Discharging enabled=yes';
                   disp('Undervoltage Event') 
                   disp(Hr)
                   P_Event(present_step)=-1;
                   %Volt_Event(present_step)=-1;
                            
            end
%             if StorP(present_step)<6500
%                      DSSText.Command = 'edit Storage.Battery kWrated=1500.0 state=Charging enabled=yes';
%              elseif StorP(present_step)>7500
%                      DSSText.Command = 'edit Storage.Battery kWrated=1500.0 state=Discharging enabled=yes';
%              end
         present_step=present_step+1;   %Advance the counter
       
    end
    
    
    
    %%% Some DSS commands to finish off the data export after solution
    %%% interval
    
    
         DSSText.command = 'closedi';
        
         DSSText.command = ['set datapath=',myDir,'\',PCSMode];
         DSSText.command = 'Export monitors SubPQ';
         DSSText.command = 'plot monitor object =SubPQ channels =(1,2)';
%         DSSText.command = 'Export monitors feederPQ';
%         DSSText.command = 'Export monitors subVI';
          DSSText.command = 'Export monitors StoragePQ';
%         DSSText.command = 'plot type=monitor Object=StoragePQ Channel=(1,2)';
%         DSSText.command = 'plot type=monitor Object=StorageVI Channel=(1)';
%end